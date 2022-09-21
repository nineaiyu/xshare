import sha1 from 'js-sha1'
import {checkContentHash, checkPreHash, getUploadSid, uploadComplete} from "@/api/upload";
import {ElMessage} from "element-plus";
import {uploadProgressStore} from "@/store";
import CryptoJs from 'crypto-js'
import encHex from 'crypto-js/enc-hex'
import {BlobToArrayBuffer, upSpeed} from "@/utils/index";

// eslint-disable-next-line no-unused-vars
function hashFileInternal(file, alog = CryptoJs.algo.SHA1.create()) {
    // 指定块的大小，这里设置为20MB,可以根据实际情况进行配置
    const chunkSize = 100 * 1024 * 1024
    let promise = Promise.resolve()
    // 使用promise来串联hash计算的顺序。因为FileReader是在事件中处理文件内容的，必须要通过某种机制来保证update的顺序是文件正确的顺序
    for (let index = 0; index < file.size; index += chunkSize) {
        promise = promise.then(() => hashBlob(file.slice(index, index + chunkSize)))
    }

    /**
     * 更新文件块的hash值
     */
    function hashBlob(blob) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader()
            reader.onload = ({target}) => {
                const wordArray = CryptoJs.lib.WordArray.create(target.result)
                // 增量更新计算结果
                alog.update(wordArray)
                resolve()
            }
            reader.onerror = function (event) {
                reject(event)
            }
            reader.readAsArrayBuffer(blob)
        })
    }

    // 使用promise返回最终的计算结果
    return promise.then(() => encHex.stringify(alog.finalize()).toUpperCase())
}

// eslint-disable-next-line no-unused-vars
async function GetFileHashProofCode2(buffer, filesize, md5_int) {

    // eslint-disable-next-line no-undef
    const start = Number(BigInt(md5_int) % BigInt(filesize))
    const end = Math.min(start + 8, filesize)
    const p_buff = buffer.slice(start, end)
    return ArrayBufferToBase64(await BlobToArrayBuffer(p_buff))
}

function ArrayBufferToBase64(buffer) {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    for (let len = bytes.byteLength, i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}

function GetFileHashProofCode(buffer, filesize, md5_int) {

    // eslint-disable-next-line no-undef
    const start = Number(BigInt(md5_int) % BigInt(filesize))
    const end = Math.min(start + 8, filesize)
    const p_buff = buffer.slice(start, end)
    return ArrayBufferToBase64(p_buff)
}


function GetFilePreHash(buffer) {
    return sha1.hex(buffer.slice(0, 1024))
}

function GetFileContentHash(buffer) {
    return sha1.hex(buffer).toUpperCase()
}

async function PreHash(file, progress) {
    const buffer = await BlobToArrayBuffer(file.slice(0, 1024))
    progress.progress = Math.ceil(buffer * 100 / file.size)
    return GetFilePreHash(buffer)
}

export async function ContentHash(file, md5_int, progress) {

    return new Promise((resolve, reject) => {
        let reader = new FileReader();

        reader.onerror = function (event) {
            reject(event)
        }
        reader.onload = async function (event) {
            const buffer = event.target.result
            ElMessage.info("文件校验中，请耐心等待")
            const conHash = GetFileContentHash(event.target.result)
            const proofCode = GetFileHashProofCode(buffer, file.size, md5_int)
            resolve({conHash, proofCode})

        }
        reader.onprogress = function (event) {
            if (event && event.loaded > 1024) {
                progress.progress = Math.ceil(event.loaded * 100 / file.size)
            }
        }
        reader.readAsArrayBuffer(file)
    })
}

function fetchProgress(url, opts = {}, onProgress) {
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
        }
        if ('onprogerss' in xhr && onProgress) {
            xhr.onprogress = onProgress; //下载
        }
        xhr.send(opts.body)
    })
}

async function ChunkedUpload(fileInfo, file, uploadExtra, partInfo, progress) {
    ElMessage.info(fileInfo.file_name + ' 不支持秒传，正在分块上传中')
    let index = 0
    let count = 0
    const start_time = Date.now();
    const chunkSize = uploadExtra.part_size
    for (let start = 0; start < file.size; start += chunkSize) {
        const chunk = file.slice(start, start + chunkSize + 1);
        // let res = await fetch(partInfo[index].upload_url, { method: "put", body: chunk})

        let res = await fetchProgress(partInfo[index].upload_url, {method: "put", body: chunk}, pr => {
            progress.progress = Math.ceil((pr.loaded + index * chunkSize) * 100 / file.size)
            progress.speed = upSpeed(start_time, file.size, progress.progress)
        })
        if (res.status !== 200) {
            count += 1
            break
        }
        // let msg = `${fileInfo.file_name}:分块第${index+1}个上传成功。共${partInfo.length}个`
        // console.log(msg)
        index += 1
    }
    if (count === 0) {
        uploadComplete(fileInfo).then(res => {
            if (res.data.check_status === true) {
                progress.progress = ''
                ElMessage.success(fileInfo.file_name + ' 上传成功')
            } else {
                ElMessage.error(fileInfo.file_name + ' 上传失败')
            }
        })
    } else {
        ElMessage.error(fileInfo.file_name + ' 上传失败，请重新上传')
    }

}


export async function UploadFile(file) {
    const fileName = file.name
    const fileSize = file.size
    const progress = uploadProgressStore()
    progress.progress = 10
    getUploadSid().then(async res => {
        ElMessage.info(fileName + ' 文件读取中')
        let hash = await PreHash(file, progress)
        let fileInfo = {
            sid: res.data.sid,
            file_name: fileName,
            file_size: fileSize,
            pre_hash: hash
        }
        progress.progress = 20
        checkPreHash(fileInfo).then(async pRes => {
            if (pRes.data.check_status === true) {
                // 秒传逻辑
                progress.progress = 30
                const md5Code = pRes.data.md5_token
                ElMessage.info(fileInfo.file_name + ' 秒传检测中')
                let hash = await ContentHash(file, md5Code, progress)
                fileInfo.proof_code = hash.proofCode
                fileInfo.content_hash = hash.conHash
                checkContentHash(fileInfo).then(async cRes => {
                    if (cRes.data.check_status === true) {
                        progress.progress = ''
                        ElMessage.success(fileName + ' 上传成功')
                    } else {
                        await ChunkedUpload(fileInfo, file, cRes.data.upload_extra, cRes.data.part_info_list, progress)
                    }
                })
            } else {
                await ChunkedUpload(fileInfo, file, pRes.data.upload_extra, pRes.data.part_info_list, progress)
            }
        })
    })
}
