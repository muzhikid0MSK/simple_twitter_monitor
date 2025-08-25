"""
跨平台构建脚本
支持在Windows上构建Linux版本，在Linux上构建Windows版本
"""
import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path


class CrossPlatformBuilder:
    """跨平台构建器"""
    
    def __init__(self):
        self.current_platform = platform.system().lower()
        self.project_name = "TwitterMonitor"
        self.version = "2.0.0"
        
        # 支持的语言
        self.languages = ["zh_CN", "en_US"]
        
        # 目标平台
        self.target_platforms = ["windows", "linux"]
        
        # 构建目录
        self.build_dir = Path("build")
        self.dist_dir = Path("dist")
        
    def check_docker(self):
        """检查Docker是否可用"""
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def build_with_docker(self, target_platform: str, language: str):
        """使用Docker构建跨平台版本"""
        print(f"🐳 使用Docker构建 {target_platform} 平台的 {language} 版本...")
        
        # 创建Dockerfile
        dockerfile_content = self.create_dockerfile(target_platform)
        dockerfile_path = Path("Dockerfile.build")
        
        with open(dockerfile_path, "w", encoding="utf-8") as f:
            f.write(dockerfile_content)
        
        # 构建Docker镜像
        image_name = f"twitter-monitor-builder-{target_platform}"
        build_cmd = [
            "docker", "build", 
            "-f", "Dockerfile.build",
            "-t", image_name,
            "."
        ]
        
        print(f"执行命令: {' '.join(build_cmd)}")
        
        try:
            subprocess.run(build_cmd, check=True)
            print("✅ Docker镜像构建成功")
            
            # 运行Docker容器进行构建
            container_name = f"builder-{target_platform}-{language}"
            run_cmd = [
                "docker", "run", "--rm",
                "--name", container_name,
                "-v", f"{Path.cwd().absolute()}:/workspace",
                "-w", "/workspace",
                "-e", f"LANGUAGE={language}",
                "-e", f"TARGET_PLATFORM={target_platform}",
                image_name,
                "python3", "build_in_container.py", language, target_platform
            ]
            
            print(f"执行命令: {' '.join(run_cmd)}")
            subprocess.run(run_cmd, check=True)
            
            # 清理Docker镜像
            subprocess.run(["docker", "rmi", image_name], check=True)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker构建失败: {e}")
            return False
        finally:
            # 清理Dockerfile
            if dockerfile_path.exists():
                dockerfile_path.unlink()
    
    def create_dockerfile(self, target_platform: str):
        """创建构建用的Dockerfile"""
        if target_platform == "windows":
            return """# Windows构建环境
FROM ubuntu:20.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    python3 \\
    python3-pip \\
    python3-dev \\
    build-essential \\
    wget \\
    curl \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# 安装PyInstaller
RUN pip3 install pyinstaller

# 设置工作目录
WORKDIR /workspace

# 复制项目文件
COPY . .

# 安装Python依赖
RUN pip3 install -r requirements.txt

# 设置默认命令
CMD ["python3", "build_in_container.py"]
"""
        else:
            return """# Linux构建环境
FROM ubuntu:20.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    python3 \\
    python3-pip \\
    python3-dev \\
    build-essential \\
    wget \\
    curl \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# 安装PyInstaller
RUN pip3 install pyinstaller

# 设置工作目录
WORKDIR /workspace

# 复制项目文件
COPY . .

# 安装Python依赖
RUN pip3 install -r requirements.txt

# 设置默认命令
CMD ["python3", "build_in_container.py"]
"""
    
    def build_all_cross_platform(self):
        """构建所有跨平台版本"""
        print("🚀 开始跨平台构建...")
        print(f"当前平台: {self.current_platform}")
        print(f"目标平台: {', '.join(self.target_platforms)}")
        print(f"支持语言: {', '.join(self.languages)}")
        print("="*60)
        
        # 检查Docker
        if not self.check_docker():
            print("❌ 未找到Docker，无法进行跨平台构建")
            print("请先安装Docker Desktop或Docker Engine")
            return
        
        # 清理构建目录
        self.clean_build_dirs()
        
        success_count = 0
        total_count = len(self.target_platforms) * len(self.languages)
        
        for target_platform in self.target_platforms:
            for language in self.languages:
                print(f"\n🌍 正在构建 {target_platform} 平台的 {language} 版本...")
                
                if self.build_with_docker(target_platform, language):
                    success_count += 1
                    print(f"✅ {target_platform} {language} 版本构建成功")
                else:
                    print(f"❌ {target_platform} {language} 版本构建失败")
                
                print("-" * 40)
        
        # 构建结果汇总
        print("\n" + "="*60)
        print("🏁 跨平台构建完成！")
        print(f"成功: {success_count}/{total_count}")
        
        if success_count == total_count:
            print("🎉 所有跨平台版本构建成功！")
            self.show_output_info()
        else:
            print("⚠️ 部分版本构建失败，请检查错误信息")
    
    def clean_build_dirs(self):
        """清理构建目录"""
        print("🧹 清理构建目录...")
        
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
            
        # 重新创建目录
        self.build_dir.mkdir(exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
        
        print("✅ 构建目录清理完成")
    
    def show_output_info(self):
        """显示输出信息"""
        print("\n📦 跨平台构建输出:")
        print(f"构建目录: {self.build_dir.absolute()}")
        print(f"发布目录: {self.dist_dir.absolute()}")
        
        for target_platform in self.target_platforms:
            platform_dir = self.dist_dir / target_platform
            if platform_dir.exists():
                print(f"\n{target_platform.upper()} 平台:")
                for language in self.languages:
                    lang_dir = platform_dir / language
                    if lang_dir.exists():
                        exe_files = list(lang_dir.glob(f"{self.project_name}_{language}*"))
                        if exe_files:
                            exe_file = exe_files[0]
                            size_mb = exe_file.stat().st_size / (1024 * 1024)
                            print(f"  {language}: {exe_file.name} ({size_mb:.1f} MB)")
        
        print("\n🎯 下一步:")
        print("1. 检查 dist 目录中的可执行文件")
        print("2. 测试不同平台和语言版本")
        print("3. 打包分发给用户")


def main():
    """主函数"""
    print("="*60)
    print("Twitter监控器 - 跨平台构建工具")
    print("="*60)
    
    # 检查Docker
    builder = CrossPlatformBuilder()
    
    if not builder.check_docker():
        print("❌ 未找到Docker")
        print("请先安装Docker Desktop或Docker Engine")
        print("\n安装说明:")
        print("- Windows: 下载Docker Desktop")
        print("- Linux: 运行 'sudo apt-get install docker.io'")
        print("- macOS: 下载Docker Desktop")
        return
    
    # 构建所有跨平台版本
    builder.build_all_cross_platform()
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
    input("\n按回车键退出...")
