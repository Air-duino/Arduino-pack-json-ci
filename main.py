# 导入requests库
import requests
import json
import hashlib
import os

packagesPath = "package_air_index.json"

GCCVersion = "12.2.1-1.2"
AirISPVersion = "1.1.1.0"
CMSISVersion = "5.7.0"
PlatformsVersion = ["0.0.1"]


def ComputeSHA256(path):
    path = "temp/" + path
    with open(path, "rb") as f:
        # 读取文件内容
        data = f.read()
        # 计算SHA256值
        sha256 = hashlib.sha256(data).hexdigest()
        # 打印SHA256值
        print("The SHA256 of", path, "is", sha256)
        return sha256


def ComputeSize(path):
    path = "temp/" + path
    # 获取文件大小，单位为字节
    file_size = os.path.getsize(path)
    # 打印文件大小
    print("The size of", path, "is", file_size, "bytes")
    return str(file_size)


def downloadFile(url):
    # 定义文件名
    filename = url.split("/")[-1]

    # 定义保存路径
    save_path = "temp/" + filename

    # 发送get请求，获取文件内容
    response = requests.get(url)

    # 判断响应状态码是否为200，表示成功
    if response.status_code == 200:
        # 打开文件，以二进制写入模式
        with open(save_path, "wb") as f:
            # 写入文件内容
            f.write(response.content)
        # 打印成功信息
        print("File downloaded and saved to", save_path)
    else:
        # 打印失败信息
        print("Failed to download file, status code:", response.status_code)


def DownloadAndCheck(url, fileName, host, suffixName):
    temp = {}
    url += fileName
    temp['host'] = host
    tempUrl = url + suffixName
    downloadFile(tempUrl)
    temp['url'] = tempUrl
    print(tempUrl)
    temp['archiveFileName'] = fileName + suffixName
    tempPath = fileName + suffixName
    temp['checksum'] = "SHA-256:" + ComputeSHA256(tempPath)
    temp['size'] = ComputeSize(tempPath)
    return temp


def GCC():
    data = {'name': "xpack-arm-none-eabi-gcc", 'version': GCCVersion}
    system = []

    def f(host, suffixName):
        url = "https://github.com/xpack-dev-tools/arm-none-eabi-gcc-xpack/releases/download/v" + GCCVersion + "/"
        fileName = "xpack-arm-none-eabi-gcc-" + GCCVersion + "-"
        return DownloadAndCheck(url, fileName, host, suffixName)

    temp = f("x86_64-mingw32", "win32-x64.zip")
    system.append(temp)
    temp = f("i686-mingw32", "win32-x64.zip")
    system.append(temp)
    temp = f("x86_64-apple-darwin", "darwin-x64.tar.gz")
    system.append(temp)
    temp = f("arm64-apple-darwin", "darwin-arm64.tar.gz")
    system.append(temp)
    temp = f("arm-linux-gnueabihf", "linux-arm.tar.gz")
    system.append(temp)
    temp = f("aarch64-linux-gnu", "linux-arm64.tar.gz")
    system.append(temp)
    temp = f("x86_64-pc-linux-gnu", "linux-x64.tar.gz")
    system.append(temp)
    data['systems'] = system
    return data


def AirISP():
    data = {'name': "AirISP", 'version': AirISPVersion}
    system = []

    def f(host, suffixName):
        url = "https://github.com/Air-duino/AirISP/releases/download/" + AirISPVersion + "/"
        fileName = "AirISP-"
        return DownloadAndCheck(url, fileName, host, suffixName)

    temp = f("x86_64-mingw32", "win-x64.zip")
    system.append(temp)
    temp = f("i686-mingw32", "win-x64.zip")
    system.append(temp)
    temp = f("x86_64-apple-darwin", "osx-x64.zip")
    system.append(temp)
    temp = f("arm64-apple-darwin", "osx-arm64.zip")
    system.append(temp)
    temp = f("arm-linux-gnueabihf", "linux-arm.zip")
    system.append(temp)
    temp = f("aarch64-linux-gnu", "linux-arm64.zip")
    system.append(temp)
    temp = f("x86_64-pc-linux-gnu", "linux-x64.zip")
    system.append(temp)
    data['systems'] = system
    print(data)
    return data


def CMSIS():
    data = {'name': "CMSIS", 'version': CMSISVersion}
    system = []

    def f(host, suffixName):
        url = "https://github.com/stm32duino/ArduinoModule-CMSIS/releases/download/" + CMSISVersion + "/"
        fileName = "CMSIS-" + CMSISVersion
        return DownloadAndCheck(url, fileName, host, suffixName)

    temp = f("x86_64-mingw32", ".tar.bz2")
    system.append(temp)
    temp = f("i686-mingw32", ".tar.bz2")
    system.append(temp)
    temp = f("x86_64-apple-darwin", ".tar.bz2")
    system.append(temp)
    temp = f("arm64-apple-darwin", ".tar.bz2")
    system.append(temp)
    temp = f("arm-linux-gnueabihf", ".tar.bz2")
    system.append(temp)
    temp = f("aarch64-linux-gnu", ".tar.bz2")
    system.append(temp)
    temp = f("x86_64-pc-linux-gnu", ".tar.bz2")
    system.append(temp)
    data['systems'] = system
    print(data)
    return data


def PlatformsAirMCU(version):
    fileName = "AirMCU-" + version + ".zip"
    url = "https://github.com/Air-duino/Arduino-AirMCU/releases/download/" + version + "/" + fileName
    downloadFile(url)
    data = {}
    data['name'] = "Air MCU"
    data['architecture'] = "AirMCU"
    data['version'] = version
    data['category'] = "Contributed"
    data['help'] = {'online': "https://github.com/Air-duino/Arduino-AirMCU"}
    data['url'] = url
    data['archiveFileName'] = fileName
    data['checksum'] = "SHA-256:" + ComputeSHA256(fileName)
    data['size'] = ComputeSize(fileName)
    data['boards'] = [{'name': "Air001"}]
    data['toolsDependencies'] = [{'packager': "AirM2M", 'name': "xpack-arm-none-eabi-gcc", 'version': GCCVersion},
                                 {'packager': "AirM2M", 'name': "CMSIS", 'version': CMSISVersion},
                                 {'packager': "AirM2M", 'name': "AirISP", 'version': AirISPVersion}]
    return data


def PackagesAirM2M():
    data = {}
    data['name'] = "AirM2M"
    data['maintainer'] = "AirM2M"
    data['websiteURL'] = "https://github.com/Air-duino"
    data['email'] = "HalfSweet@HalfSweet.cn"
    data['help'] = {'online': "https://github.com/Air-duino"}
    platforms = []
    for item in PlatformsVersion:
        platforms.append(PlatformsAirMCU(item))
    data['platforms'] = platforms
    tools = [GCC(), CMSIS(), AirISP()]
    data['tools'] = tools
    return data


def Encode():
    data = {}
    data['packages'] = [PackagesAirM2M()]
    json_str = json.dumps(data, indent=2)
    with open(packagesPath, "w+") as f:
        f.write(json_str)
    return json_str


def main():
    print(Encode())


if __name__ == '__main__':
    main()
