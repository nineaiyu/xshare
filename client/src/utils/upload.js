import sha1 from 'js-sha1'
import {checkContentHash, checkPreHash, getUploadSid, uploadComplete} from "@/api/upload";
import {ElMessage} from "element-plus";
import {uploadStore} from "@/store";
import {BlobToArrayBuffer, diskSize, upSpeed} from "@/utils/index";


function ArrayBufferToBase64(buffer) {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    for (let len = bytes.byteLength, i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}


function GetFilePreHash(buffer) {
    return sha1.hex(buffer.slice(0, 1024))
}


async function PreHash(file, progress) {
    const buffer = await BlobToArrayBuffer(file.slice(0, 1024))
    progress.progress = Math.ceil(buffer.byteLength * 100 / file.size)
    return GetFilePreHash(buffer)
}

async function GetFileHashProofCode(file, filesize, md5_int) {
    // eslint-disable-next-line no-undef
    const start = Number(BigInt(md5_int) % BigInt(filesize))
    const end = Math.min(start + 8, filesize)
    const p_buff = file.slice(start, end)
    return ArrayBufferToBase64(await BlobToArrayBuffer(p_buff))
}


export async function ContentHash(file, md5_int, progress) {

    return new Promise((resolve, reject) => {
        const chunkSize = 50 * 1024 * 1024
        let promise = Promise.resolve()
        for (let index = 0; index < file.size; index += chunkSize) {
            promise = promise.then(() => hashBlob(file.slice(index, index + chunkSize)))
        }
        let count = 0
        const hash = sha1.create()

        function hashBlob(blob) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader()
                reader.onload = ({target}) => {
                    hash.update(target.result)
                    count += 1
                    resolve()
                }
                reader.onerror = function (event) {
                    reject(event)
                }
                reader.onprogress = function (event) {
                    if (event) {
                        progress.progress = Math.ceil((event.loaded + count * chunkSize) * 100 / progress.file_size)
                    }
                }
                reader.readAsArrayBuffer(blob)
            })
        }

        promise.then(async () => {
            const conHash = hash.hex().toUpperCase()
            const proofCode = await GetFileHashProofCode(file, progress.file_size, md5_int)
            resolve({conHash, proofCode})
        }).catch(() => {
            reject()
        })
    })
}

function fetchProgress(fileInfo, url, opts = {}, onProgress) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open(opts.method, url);
        for (let key in opts.headers || {}) {
            xhr.setRequestHeader(key, opts.headers[key]);
        }
        xhr.onload = e => resolve(e.target)
        xhr.onerror = reject;
        if (xhr.upload && onProgress) {
            xhr.upload.onprogress = onProgress; //上传
            if (fileInfo.status === 3) {
                xhr.abort()
                reject()
            }
        }
        if ('onprogerss' in xhr && onProgress) {
            xhr.onprogress = onProgress; //下载
            if (fileInfo.status === 3) {
                xhr.abort()
                reject()
            }
        }
        xhr.send(opts.body)
    })
}

async function ChunkedUpload(fileInfo, fileHashInfo, uploadExtra, partInfo, resolve = null, reject = null) {
    // ElMessage.info(fileInfo.file_name + ' 不支持秒传，正在分块上传中')
    const progress = fileInfo.progress
    progress.speed = '上传中'
    let count = 0
    const partNumber = 20  // 统计20分块的下载速度
    const chunkSize = uploadExtra.part_size

    for (let index = 0; index < partInfo.length; index++) {
        const chunk = fileInfo.file.slice(index * chunkSize, (index + 1) * chunkSize);
        // let res = await fetch(partInfo[index].upload_url, { method: "put", body: chunk})
        let res = await fetchProgress(fileInfo, partInfo[index].upload_url, {method: "put", body: chunk}, pr => {
            progress.progress = Math.ceil((pr.loaded + index * chunkSize) * 100 / progress.file_size)
            progress.upload_size = pr.loaded + index * chunkSize
            progress.percent.push({time: Date.now(), progress: progress.progress})
            if (progress.progress > 0) {
                let percent = progress.percent;
                if (percent.length > partNumber) {
                    percent.shift()
                    progress.speed = diskSize(upSpeed(percent[percent.length - partNumber].time, progress.file_size, progress.progress - percent[percent.length - partNumber].progress))
                } else {
                    if (percent.length > 1) {
                        progress.speed = diskSize(upSpeed(percent[0].time, progress.file_size, progress.progress))
                    }
                }
            }
        })
        if (res.status !== 200) {
            count += 1
            break
        }
    }

    if (count === 0) {
        uploadComplete(fileHashInfo).then(res => {
            if (res.data.check_status === true) {
                // ElMessage.success(fileInfo.file_name + ' 上传成功')
                if (resolve) {
                    resolve(fileHashInfo.file_name + ' 上传成功')
                }
                progress.progress = 100
                progress.speed = '上传成功'
                fileInfo.file = null
            } else {
                ElMessage.error(fileHashInfo.file_name + ' 上传失败')
                reject()
            }
        }).catch((e) => {
            reject(e)
        })
    } else {
        ElMessage.error(fileHashInfo.file_name + ' 上传失败，请重新上传')
        reject()
    }

}

// 多线程上传操作


function multiRun(upload, keyList, func) {
    const processNumber = upload.processNumber
    const promise = upload.promise
    for (let i = 0; i < processNumber - promise.length; i++) {
        promise.push(Promise.resolve())
    }
    let reduceNumber = promise.length - processNumber
    if (reduceNumber > 0) {
        upload.promise = promise.slice(0, reduceNumber)
    }
    for (let j = 0; j < keyList.length; j += processNumber) {
        for (let i = 0; i < processNumber; i++) {
            if (i + j < keyList.length) {
                promise[(j + i) % processNumber] = promise[(j + i) % processNumber].then(() => func(keyList[i + j])).catch(({
                                                                                                                                fileInfo,
                                                                                                                                err
                                                                                                                            }) => {
                    if (fileInfo.status === 3) {
                        console.log(fileInfo.file.name, '取消上传')
                    } else {
                        fileInfo.status = 0
                        fileInfo.failTryCount -= 1
                        if (fileInfo.failTryCount < 1) {
                            fileInfo.status = 4
                            ElMessage.error(`${fileInfo.file.name} 超过最大重试次数，停止上传`)
                        } else {
                            ElMessage.error(`${fileInfo.file.name} 上传失败，正在重试`)
                            console.log(fileInfo.file.name, err)
                            multiUpload()
                        }
                    }
                })
            }
        }
    }
}


function uploadAsync(fileInfo) {
    const progress = fileInfo.progress
    const file = fileInfo.file
    return new Promise((resolve, reject) => {
        if (fileInfo.status === 0) {
            fileInfo.status = 1
        } else {
            return resolve()
        }
        progress.progress = 10
        getUploadSid().then(async res => {
            // ElMessage.info(fileName + ' 文件读取中')
            progress.speed = '文件读取中'
            let hash = await PreHash(file, progress)
            let fileHashInfo = {
                sid: res.data.sid,
                file_name: progress.file_name,
                file_size: progress.file_size,
                pre_hash: hash
            }
            progress.progress = 20
            checkPreHash(fileHashInfo).then(async pRes => {
                if (pRes.data.check_status === true) {
                    // 秒传逻辑
                    progress.progress = 30
                    const md5Code = pRes.data.md5_token
                    progress.speed = '文件校验中'
                    // ElMessage.info(fileInfo.file_name + ' 秒传检测中')
                    let hash = await ContentHash(file, md5Code, progress)
                    fileHashInfo.proof_code = hash.proofCode
                    fileHashInfo.content_hash = hash.conHash
                    checkContentHash(fileHashInfo).then(async cRes => {
                        if (cRes.data.check_status === true) {
                            progress.progress = 100
                            progress.upload_size = progress.file_size
                            progress.speed = '秒传成功'
                            // ElMessage.success(fileName + ' 上传成功')
                            fileInfo.status = 2
                            fileInfo.upload_time = new Date()
                            fileInfo.file = null
                            multiUpload()
                            resolve()
                        } else {
                            return await ChunkedUpload(fileInfo, fileHashInfo, cRes.data.upload_extra, cRes.data.part_info_list, () => {
                                fileInfo.status = 2
                                fileInfo.upload_time = new Date()
                                multiUpload()
                                resolve()
                            }, (err) => {
                                reject({fileInfo, err})
                            })
                        }
                    }).catch((err) => {
                        reject({fileInfo, err})
                    })
                } else {
                    return await ChunkedUpload(fileInfo, fileHashInfo, pRes.data.upload_extra, pRes.data.part_info_list, () => {
                        fileInfo.status = 2
                        fileInfo.upload_time = new Date()
                        multiUpload()
                        resolve()
                    }, (err) => {
                        reject({fileInfo, err})
                    })
                }
            }).catch((err) => {
                reject({fileInfo, err})
            })
        }).catch((err) => {
            reject({fileInfo, err})
        })
    })
}

export function multiUpload() {
    const upload = uploadStore()
    const readFileList = []
    upload.multiFileList.forEach(res => {
        if (res.status === 0) {
            readFileList.push(res)
        }
    })
    if (readFileList.length > 0) {
        multiRun(upload, readFileList.slice(0, upload.processNumber), uploadAsync)
    }
}

export function addUploadFile(raw) {
    const upload = uploadStore()
    const uploadProgress = {
        progress: 0,
        file_id: '',
        file_name: raw.name,
        percent: [],
        speed: '0 MB',
        file_size: raw.size,
        upload_size: 0,
        upload_time: new Date()
    }
    // status上传状态 0 队列，1 上传中，2 上传成功 ， 3 取消上传
    // failTryCount 失败上传次数, 没上传一次，自动减去已，当为0的时候，停止上传
    upload.multiFileList.push({file: raw, progress: uploadProgress, status: 0, failTryCount: 3, uid: raw.uid})
    multiUpload()
}

