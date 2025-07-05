#!/usr/bin/env python3
"""
TopShopE 代码质量检查脚本
检查语法错误、导入问题等
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Dict

class CodeChecker:
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def check_python_file(self, file_path: str) -> bool:
        """检查Python文件的语法"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 尝试解析AST
            ast.parse(content)
            return True
        except SyntaxError as e:
            self.errors.append(f"语法错误 {file_path}:{e.lineno}: {e.msg}")
            return False
        except Exception as e:
            self.errors.append(f"解析错误 {file_path}: {str(e)}")
            return False
    
    def check_imports(self, file_path: str) -> bool:
        """检查导入语句"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._check_import_name(alias.name, file_path)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self._check_import_name(node.module, file_path)
            
            return True
        except Exception as e:
            self.errors.append(f"导入检查错误 {file_path}: {str(e)}")
            return False
    
    def _check_import_name(self, import_name: str, file_path: str):
        """检查具体的导入名称"""
        # 检查app模块的导入
        if import_name.startswith('app.'):
            parts = import_name.split('.')
            if len(parts) >= 2:
                module_path = Path('backend') / '/'.join(parts[1:])
                if not (module_path.with_suffix('.py').exists() or 
                       (module_path / '__init__.py').exists()):
                    self.warnings.append(f"可能的导入错误 {file_path}: {import_name}")
    
    def check_directory(self, directory: str) -> Dict[str, int]:
        """检查目录中的所有Python文件"""
        stats = {'total': 0, 'errors': 0, 'warnings': 0}
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    stats['total'] += 1
                    
                    # 检查语法
                    if not self.check_python_file(file_path):
                        stats['errors'] += 1
                    
                    # 检查导入
                    self.check_imports(file_path)
        
        stats['warnings'] = len(self.warnings)
        return stats
    
    def print_report(self):
        """打印检查报告"""
        print("🔍 TopShopE 代码质量检查报告")
        print("=" * 50)
        
        if self.errors:
            print(f"❌ 发现 {len(self.errors)} 个错误:")
            for error in self.errors:
                print(f"   {error}")
            print()
        
        if self.warnings:
            print(f"⚠️ 发现 {len(self.warnings)} 个警告:")
            for warning in self.warnings:
                print(f"   {warning}")
            print()
        
        if not self.errors and not self.warnings:
            print("✅ 代码检查通过，没有发现错误或警告！")
        else:
            print(f"📊 总结: {len(self.errors)} 个错误, {len(self.warnings)} 个警告")

def main():
    """主函数"""
    checker = CodeChecker()
    
    # 检查后端代码
    print("🔍 检查后端代码...")
    backend_stats = checker.check_directory('backend')
    print(f"   检查了 {backend_stats['total']} 个Python文件")
    
    # 检查测试文件
    print("🔍 检查测试文件...")
    if os.path.exists('test_mvp.py'):
        checker.check_python_file('test_mvp.py')
        checker.check_imports('test_mvp.py')
    
    # 打印报告
    checker.print_report()
    
    # 返回状态码
    if checker.errors:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main() 