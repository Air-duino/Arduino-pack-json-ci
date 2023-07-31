# 导入requests库
import requests
import json
import hashlib
import os

packagesPath = "package_air_index.json"
packagesCNPath = "package_air_cn_index.json"

GCCVersion = "12.2.1-1.2"
AirISPVersion = ""  # 不定义具体的版本，在GetAirISPVersion函数中创造
CMSISVersion = "5.7.0"
PlatformsVersion = []


def GetAirISPVersion():
    url = "https://api.github.com/repos/Air-duino/AirISP/releases"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        tags = []
        for release in data:
            tag = release["tag_name"]
            tags.append(tag)
        global AirISPVersion
        AirISPVersion = str(tags[0])
    else:
        print(f"Request failed: {response.status_code}")


def GetRepoVersion(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        tags = []
        for release in data:
            tag = release["tag_name"]
            tags.append(tag)
        return tags
    else:
        print(f"Request failed: {response.status_code}")


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
    tempCn = {}
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

    tempCn = temp
    tempCn['url'] = "https://arduino.luatos.com/" + fileName + suffixName
    return temp, tempCn


def GCC():
    data = {'name': "xpack-arm-none-eabi-gcc", 'version': GCCVersion}
    dataCn = data
    system = []
    systemCn = []

    def f(host, suffixName):
        url = "https://github.com/xpack-dev-tools/arm-none-eabi-gcc-xpack/releases/download/v" + GCCVersion + "/"
        fileName = "xpack-arm-none-eabi-gcc-" + GCCVersion + "-"
        return DownloadAndCheck(url, fileName, host, suffixName)

    temp, tempCn = f("x86_64-mingw32", "win32-x64.zip")
    system.append(temp)
    systemCn.append(tempCn)
    temp, tempCn = f("i686-mingw32", "win32-x64.zip")
    system.append(temp)
    systemCn.append(tempCn)
    temp, tempCn = f("x86_64-apple-darwin", "darwin-x64.tar.gz")
    system.append(temp)
    systemCn.append(tempCn)
    temp, tempCn = f("arm64-apple-darwin", "darwin-arm64.tar.gz")
    system.append(temp)
    systemCn.append(tempCn)
    temp, tempCn = f("arm-linux-gnueabihf", "linux-arm.tar.gz")
    system.append(temp)
    systemCn.append(tempCn)
    temp, tempCn = f("aarch64-linux-gnu", "linux-arm64.tar.gz")
    system.append(temp)
    systemCn.append(tempCn)
    temp, tempCn = f("x86_64-pc-linux-gnu", "linux-x64.tar.gz")
    system.append(temp)
    systemCn.append(tempCn)
    data['systems'] = system
    dataCn['systems'] = systemCn
    return data, dataCn


def AirISP():
    data = {'name': "AirISP", 'version': AirISPVersion}
    dataCn = data
    system = []
    systemCn = []

    def f(host, suffixName):
        url = "https://github.com/Air-duino/AirISP/releases/download/" + AirISPVersion + "/"
        fileName = "AirISP-"
        return DownloadAndCheck(url, fileName, host, suffixName)

    temp, tempCn = f("x86_64-mingw32", "win-x64.zip")
    system.append(temp)
    systemCn.append(tempCn)
    temp, tempCn = f("i686-mingw32", "win-x64.zip")
    system.append(temp)
    systemCn.append(tempCn)
    temp, tempCn = f("x86_64-apple-darwin", "osx-x64.tar")
    system.append(temp)
    systemCn.append(tempCn)
    temp, tempCn = f("arm64-apple-darwin", "osx-arm64.tar")
    system.append(temp)
    systemCn.append(tempCn)
    temp, tempCn = f("arm-linux-gnueabihf", "linux-arm.tar")
    system.append(temp)
    systemCn.append(tempCn)
    temp, tempCn = f("aarch64-linux-gnu", "linux-arm64.tar")
    system.append(temp)
    systemCn.append(tempCn)
    temp, tempCn = f("x86_64-pc-linux-gnu", "linux-x64.tar")
    system.append(temp)
    systemCn.append(tempCn)

    data['systems'] = system
    dataCn['systems'] = systemCn
    return data, dataCn


def CMSIS():
    data = {'name': "CMSIS", 'version': CMSISVersion}
    dataCn = data
    system = []
    systemCn = []

    def f(host, suffixName):
        url = "https://github.com/stm32duino/ArduinoModule-CMSIS/releases/download/" + CMSISVersion + "/"
        fileName = "CMSIS-" + CMSISVersion
        return DownloadAndCheck(url, fileName, host, suffixName)

    temp, tempCn = f("x86_64-mingw32", ".tar.bz2")
    system.append(temp)
    systemCn.append(tempCn)
    temp, tempCn = f("i686-mingw32", ".tar.bz2")
    system.append(temp)
    systemCn.append(tempCn)
    temp, tempCn = f("x86_64-apple-darwin", ".tar.bz2")
    system.append(temp)
    systemCn.append(tempCn)
    temp, tempCn = f("arm64-apple-darwin", ".tar.bz2")
    system.append(temp)
    systemCn.append(tempCn)
    temp, tempCn = f("arm-linux-gnueabihf", ".tar.bz2")
    system.append(temp)
    systemCn.append(tempCn)
    temp, tempCn = f("aarch64-linux-gnu", ".tar.bz2")
    system.append(temp)
    systemCn.append(tempCn)
    temp, tempCn = f("x86_64-pc-linux-gnu", ".tar.bz2")
    system.append(temp)
    systemCn.append(tempCn)

    data['systems'] = system
    dataCn['systems'] = systemCn
    return data, dataCn


def PlatformsAirMCU(version):
    fileName = "AirMCU-" + version + ".zip"
    url = "https://github.com/Air-duino/Arduino-AirMCU/releases/download/" + version + "/" + fileName
    downloadFile(url)
    data = {}
    dataCn = {}
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
    dataCn = data
    dataCn['url'] = "https://arduino.luatos.com/" + fileName
    return data, dataCn


def PackagesAirM2M():
    data = {}
    dataCn = {}
    data['name'] = "AirM2M"
    data['maintainer'] = "AirM2M"
    data['websiteURL'] = "https://github.com/Air-duino"
    data['email'] = "HalfSweet@HalfSweet.cn"
    data['help'] = {'online': "https://github.com/Air-duino"}
    platforms = []
    platformsCn = []

    PlatformsVersion.extend(GetRepoVersion("Air-duino", "Arduino-AirMCU"))
    for item in PlatformsVersion:
        temp, tempCn = PlatformsAirMCU(item)
        platforms.append(temp)
        platformsCn.append(tempCn)
    data['platforms'] = platforms
    tools = []
    toolsCn = []

    temp, tempCn = GCC()
    tools.append(temp)
    toolsCn.append(tempCn)

    temp, tempCn = CMSIS()
    tools.append(temp)
    toolsCn.append(tempCn)

    temp, tempCn = AirISP()
    tools.append(temp)
    toolsCn.append(tempCn)

    data['tools'] = tools
    dataCn = data
    dataCn['tools'] = toolsCn
    return data, dataCn


def Encode():
    data = {}
    dataCn = {}
    temp, tempCn = PackagesAirM2M()
    data['packages'] = [temp]
    dataCn['packages'] = [tempCn]
    json_str = json.dumps(data, indent=2)
    with open(packagesPath, "w+") as f:
        f.write(json_str)
    json_str_cn = json.dumps(dataCn, indent=2)
    with open(packagesCNPath, "w+") as f:
        f.write(json_str_cn)
    return json_str, json_str_cn


def main():
    GetAirISPVersion()
    print(Encode())


if __name__ == '__main__':
    main()
