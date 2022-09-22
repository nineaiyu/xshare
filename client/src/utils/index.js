export function diskSize(num) {
    if (num === 0) return '0 B';
    let k = 1024; //设定基础容量大小
    let sizeStr = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']; //容量单位
    let i = 0; //单位下标和次幂
    for (let l = 0; l < 9; l++) {   //因为只有8个单位所以循环八次
        if (num / Math.pow(k, l) < 1) { //判断传入数值 除以 基础大小的次幂 是否小于1，这里小于1 就代表已经当前下标的单位已经不合适了所以跳出循环
            break; //小于1跳出循环
        }
        i = l; //不小于1的话这个单位就合适或者还要大于这个单位 接着循环
    }
    return (num / Math.pow(k, i)).toFixed(1) + ' ' + sizeStr[i];  //循环结束 或 条件成立 返回字符
}


export function upSpeed(start_time, file_size, percent) {
    const now_time = Date.now();
    return file_size * percent * 10 / (now_time - start_time)
}

export function formatTime(time) {
    if (time && (typeof time === 'string')) {
        time = time.split('+')[0].split(".")[0].split("T");
        return time[0] + " " + time[1]
    } else
        return time;
}

export function BlobToArrayBuffer(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onloadend = function (event) {
            resolve(event.target.result)
        };
        reader.onerror = function (event) {
            reject(event)
        }
        reader.readAsArrayBuffer(file);
    })

}

export function downloadFile(url) {
    const iframe = document.createElement("iframe");
    iframe.style.display = "none";  // 防止影响页面
    iframe.style.height = 0;  // 防止影响页面
    iframe.src = url;
    document.body.appendChild(iframe);
    setTimeout(() => {
        iframe.remove();
    }, 5 * 60 * 1000);
}

export function getLocationOrigin() {
    const hash = window.location.hash
    let origin = window.location.origin
    if (hash && hash.startsWith('#/')) {
        origin = origin + '/#'
    }
    return origin + '/'
}

export function getRandomNum(Min, Max) {
    const Range = Max - Min;
    const Rand = Math.random();
    return (Min + Math.round(Rand * Range));
}

export function getRandomStr(strLength = 32) {
    const SIGNING_v1 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'//36
    const SIGNING_v5 = 'abcdefghigklmnopqrstuvwxyz'//26
    let randomStr = SIGNING_v1 + SIGNING_v5
    let randomCode = ''
    for (let i = 0; i < strLength; i++) {
        randomCode = randomCode + randomStr[getRandomNum(0, randomStr.length - 1)]
    }
    return randomCode
}

function randomColor() {
    let random = '#'
    for (let i = 0; i < 6; i++) {
        random += parseInt(Math.random() * 15).toString(16)  //随机数取整，并转换成16进制
    }
    return random    //返回随机数
}

export function createBase64(str) {
    if (str.length > 1) {
        str = str[getRandomNum(0, str.length - 1)]
    }
    const can = document.createElement("canvas");
    const width = 160;
    const height = 160;
    Object.assign(can, {width, height});

    const cans = can.getContext("2d");
    if (cans) {
        cans.font = "130px Arial";
        // cans.fillStyle = "rgb(8,115,199)";
        cans.shadowBlur = 20;
        cans.shadowColor = "black";
        cans.fillStyle = randomColor();
        cans.textAlign = "center";
        cans.textBaseline = "middle";
        cans.fillText(str, width / 2, height / 2 + 10);
    }
    return can.toDataURL("image/png");
}
