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
    return diskSize(file_size * percent * 10 / (now_time - start_time))
}

export function formatTime(time) {
    if (time) {
        time = time.split(".")[0].split("T");
        return time[0] + " " + time[1]
    } else
        return '';
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

