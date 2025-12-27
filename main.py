import requests
from typing import Optional, Union
import os


class QQAvatar:
    """QQ头像获取工具（简化版，不需要Pillow）"""

    def __init__(self):
        # 基础URL
        self.normal_url_template = "http://q{server}.qlogo.cn/g?b=qq&nk={qq}&s={size}"
        self.hd_url_template = "http://q.qlogo.cn/headimg_dl?dst_uin={qq}&spec={size}&img_type=jpg"

    def get_avatar_url(self, qq: Union[str, int], hd: bool = True, size: int = 640) -> str:
        """
        获取QQ头像URL

        Args:
            qq: QQ号码
            hd: True使用高清接口，False使用普通接口
            size: 头像尺寸（高清最高640，普通最高140）

        Returns:
            str: 头像URL
        """
        qq_str = str(qq)

        if hd:
            # 高清接口
            if size > 640:
                size = 640
            return self.hd_url_template.format(qq=qq_str, size=size)
        else:
            # 普通接口
            if size > 140:
                size = 140
            # 根据QQ号选择服务器
            server = '1' if int(qq_str) % 2 == 0 else '2'
            return self.normal_url_template.format(server=server, qq=qq_str, size=size)

    def download_avatar(self, qq: Union[str, int], save_path: str = None,
                        hd: bool = True, size: int = 640) -> bool:
        """
        下载QQ头像到本地

        Args:
            qq: QQ号码
            save_path: 保存路径，如不指定则保存为当前目录
            hd: 是否使用高清接口
            size: 头像尺寸

        Returns:
            bool: 是否下载成功
        """
        url = self.get_avatar_url(qq, hd=hd, size=size)

        # 设置默认保存路径
        if save_path is None:
            suffix = "_hd.jpg" if hd else ".png"
            save_path = f"qq_{qq}{suffix}"

        try:
            # 获取头像
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # 检查请求是否成功

            # 确保目录存在
            os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)

            # 保存文件
            with open(save_path, 'wb') as f:
                f.write(response.content)

            print(f"✓ 头像已保存: {save_path} ({len(response.content)} bytes)")
            return True

        except requests.exceptions.RequestException as e:
            print(f"✗ 下载失败: {e}")
            return False
        except Exception as e:
            print(f"✗ 保存失败: {e}")
            return False

    def check_avatar_exists(self, qq: Union[str, int], hd: bool = True) -> bool:
        """
        检查QQ头像是否存在

        Args:
            qq: QQ号码
            hd: 是否检查高清头像

        Returns:
            bool: 头像是否存在
        """
        url = self.get_avatar_url(qq, hd=hd)

        try:
            response = requests.head(url, timeout=5)
            return response.status_code == 200
        except:
            return False

    def batch_download(self, qq_list: list, output_dir: str = "avatars",
                       hd: bool = True, size: int = 640):
        """
        批量下载QQ头像

        Args:
            qq_list: QQ号码列表
            output_dir: 输出目录
            hd: 是否使用高清接口
            size: 头像尺寸
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        print(f"开始批量下载 {len(qq_list)} 个头像...")
        success_count = 0

        for i, qq in enumerate(qq_list, 1):
            print(f"[{i}/{len(qq_list)}] 下载 QQ: {qq}...", end=" ")

            # 构造保存路径
            suffix = "_hd.jpg" if hd else ".png"
            save_path = os.path.join(output_dir, f"{qq}{suffix}")

            if self.download_avatar(qq, save_path, hd, size):
                success_count += 1

        print(f"\n下载完成！成功: {success_count}/{len(qq_list)}")


# 使用示例
if __name__ == "__main__":
    # 创建实例
    qq_avatar = QQAvatar()

    # 示例QQ号（请替换为实际QQ号）
    test_qq = "123456789"

    print("=== 单个头像下载示例 ===")

    # 获取URL
    hd_url = qq_avatar.get_avatar_url(test_qq, hd=True, size=640)
    normal_url = qq_avatar.get_avatar_url(test_qq, hd=False, size=100)

    print(f"高清头像URL: {hd_url}")
    print(f"普通头像URL: {normal_url}")

    # 检查头像是否存在
    if qq_avatar.check_avatar_exists(test_qq):
        print("✓ 头像存在")

        # 下载高清头像
        print("\n下载高清头像...")
        qq_avatar.download_avatar(test_qq, "test_hd.jpg", hd=True, size=640)

        # 下载普通头像
        print("\n下载普通头像...")
        qq_avatar.download_avatar(test_qq, "test_normal.png", hd=False, size=100)
    else:
        print("✗ 头像不存在或无法访问")

    print("\n=== 批量下载示例 ===")
    # 批量下载（示例QQ号列表）
    qq_list = ["10001", "10002", "10003"]  # 请替换为实际QQ号
    # qq_avatar.batch_download(qq_list, output_dir="my_avatars")

    print("\n=== 常用尺寸示例 ===")
    # 显示不同尺寸的URL
    sizes = {
        "极小": 40,
        "小": 100,
        "中": 140,
        "大": 200,
        "高清": 640
    }

    for name, size in sizes.items():
        url = qq_avatar.get_avatar_url(test_qq, hd=(size > 140), size=size)
        print(f"{name}({size}x{size}): {url}")