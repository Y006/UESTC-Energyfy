#!/usr/bin/env python3
"""
配置验证脚本
用于测试配置文件是否正确，避免部署后才发现问题
"""
import json
import sys
import re
from pathlib import Path


def print_header(title):
    """打印标题"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def print_success(msg):
    """打印成功消息"""
    print(f"✅ {msg}")


def print_error(msg):
    """打印错误消息"""
    print(f"❌ {msg}", file=sys.stderr)


def print_warning(msg):
    """打印警告消息"""
    print(f"⚠️  {msg}")


def print_info(msg):
    """打印信息消息"""
    print(f"ℹ️  {msg}")


def validate_email(email):
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_hostname(hostname):
    """验证主机名格式"""
    pattern = r'^[a-zA-Z0-9-]{1,63}(\.[a-zA-Z0-9-]{1,63})*$'
    return re.match(pattern, hostname) is not None


def test_smtp_connection(config):
    """测试SMTP连接"""
    print_info("测试 SMTP 连接...")
    try:
        import smtplib
        smtp_config = config['smtp']
        
        # 创建连接
        if smtp_config['security'] == 'ssl':
            server = smtplib.SMTP_SSL(
                smtp_config['server'],
                smtp_config['port'],
                timeout=10
            )
        else:
            server = smtplib.SMTP(
                smtp_config['server'],
                smtp_config['port'],
                timeout=10
            )
            if smtp_config['security'] == 'tls':
                server.starttls()
        
        # 测试登录
        server.login(smtp_config['username'], smtp_config['password'])
        server.quit()
        
        print_success("SMTP 连接测试成功")
        return True
    except smtplib.SMTPAuthenticationError:
        print_error("SMTP 认证失败！请检查用户名和密码（授权码）")
        return False
    except smtplib.SMTPException as e:
        print_error(f"SMTP 错误: {e}")
        return False
    except Exception as e:
        print_error(f"连接失败: {e}")
        return False


def test_server_chan(uid, sendkey):
    """测试 Server酱 连接"""
    print_info("测试 Server酱 连接...")
    try:
        import requests
        url = f"https://{uid}.push.ft07.com/send/{sendkey}.send"
        data = {
            "title": "UESTC-Energyfy 配置测试",
            "desp": "这是一条测试消息，如果你收到了，说明配置成功！"
        }
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get('code') == 0:
            print_success("Server酱 测试消息已发送，请检查手机")
            return True
        else:
            print_error(f"Server酱 返回错误: {result.get('message')}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Server酱 连接失败: {e}")
        return False
    except Exception as e:
        print_error(f"测试失败: {e}")
        return False


def validate_config(config_path):
    """验证配置文件"""
    print_header("配置文件验证")
    
    # 检查文件是否存在
    if not config_path.exists():
        print_error(f"配置文件不存在: {config_path}")
        return False
    
    print_success(f"找到配置文件: {config_path}")
    
    # 读取配置文件
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print_success("配置文件格式正确")
    except json.JSONDecodeError as e:
        print_error(f"JSON 格式错误: {e}")
        return False
    except Exception as e:
        print_error(f"读取失败: {e}")
        return False
    
    # 验证必需字段
    required_fields = ['username', 'password', 'check_interval', 'alert_balance', 'smtp', 'queries']
    missing_fields = [f for f in required_fields if f not in config]
    
    if missing_fields:
        print_error(f"缺少必需字段: {', '.join(missing_fields)}")
        return False
    
    print_success("所有必需字段存在")
    
    # 验证基本配置
    print("\n" + "-"*60)
    print("基本配置:")
    print(f"  学号: {config['username']}")
    print(f"  检查间隔: {config['check_interval']} 秒")
    print(f"  告警阈值: {config['alert_balance']} 元")
    
    if config['check_interval'] < 0:
        print_error("检查间隔不能为负数")
        return False
    
    if config['check_interval'] > 0 and config['check_interval'] < 300:
        print_warning("检查间隔过短（< 5分钟），可能导致账号被冻结")
    
    if config['alert_balance'] < 0:
        print_error("告警阈值不能为负数")
        return False
    
    # 验证 SMTP 配置
    print("\n" + "-"*60)
    print("SMTP 配置:")
    smtp = config['smtp']
    
    required_smtp = ['server', 'port', 'username', 'password', 'security']
    missing_smtp = [f for f in required_smtp if f not in smtp]
    
    if missing_smtp:
        print_error(f"SMTP 配置缺少字段: {', '.join(missing_smtp)}")
        return False
    
    print(f"  服务器: {smtp['server']}")
    print(f"  端口: {smtp['port']}")
    print(f"  用户名: {smtp['username']}")
    print(f"  安全协议: {smtp['security']}")
    
    if not validate_hostname(smtp['server']):
        print_warning("SMTP 服务器地址格式可能不正确")
    
    if smtp['port'] < 1 or smtp['port'] > 65535:
        print_error("SMTP 端口号必须在 1-65535 之间")
        return False
    
    if not validate_email(smtp['username']):
        print_warning("SMTP 用户名不是有效的邮箱地址")
    
    if smtp['security'] not in ['ssl', 'tls', 'none']:
        print_error("安全协议必须是 ssl、tls 或 none")
        return False
    
    # 验证查询配置
    print("\n" + "-"*60)
    print("查询配置:")
    
    queries = config['queries']
    if not queries:
        print_error("至少需要配置一个查询")
        return False
    
    print(f"  监控房间数: {len(queries)}")
    
    for i, query in enumerate(queries):
        print(f"\n  房间 {i+1}:")
        
        if 'room_name' not in query:
            print_error(f"    缺少 room_name 字段")
            return False
        
        print(f"    房间号: {query['room_name']}")
        
        if 'recipients' not in query or not query['recipients']:
            print_error(f"    至少需要一个收件人")
            return False
        
        print(f"    邮件收件人数: {len(query['recipients'])}")
        
        for email in query['recipients']:
            if not validate_email(email):
                print_error(f"    无效的邮箱地址: {email}")
                return False
        
        # 验证 Server酱 配置
        if 'server_chan' in query:
            sc = query['server_chan']
            if sc.get('enabled'):
                print(f"    Server酱: 已启用")
                if 'recipients' not in sc or not sc['recipients']:
                    print_warning(f"    Server酱已启用但没有收件人")
                else:
                    print(f"    Server酱收件人数: {len(sc['recipients'])}")
            else:
                print(f"    Server酱: 未启用")
    
    print_success("\n配置文件验证通过")
    return config


def main():
    """主函数"""
    print_header("UESTC-Energyfy 配置验证工具")
    
    # 查找配置文件
    config_path = Path('config.json')
    
    if not config_path.exists():
        print_error("未找到 config.json")
        print_info("请先创建配置文件，或使用 -c 参数指定配置文件路径")
        return 1
    
    # 验证配置
    config = validate_config(config_path)
    if not config:
        return 1
    
    # 询问是否测试连接
    print("\n" + "="*60)
    print("是否测试实际连接？这将：")
    print("  1. 测试 SMTP 邮箱登录")
    print("  2. 如果启用了 Server酱，发送一条测试消息")
    print()
    
    try:
        choice = input("是否继续？(y/N): ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\n")
        print_info("已取消")
        return 0
    
    if choice not in ['y', 'yes']:
        print_info("跳过连接测试")
        print_success("\n配置验证完成！")
        return 0
    
    # 测试 SMTP
    print_header("连接测试")
    smtp_ok = test_smtp_connection(config)
    
    # 测试 Server酱
    server_chan_ok = True
    for query in config['queries']:
        sc = query.get('server_chan', {})
        if sc.get('enabled') and sc.get('recipients'):
            for recipient in sc['recipients']:
                uid = recipient.get('uid')
                sendkey = recipient.get('sendkey')
                if uid and sendkey:
                    if not test_server_chan(uid, sendkey):
                        server_chan_ok = False
                    break  # 只测试第一个
            break  # 只测试第一个查询
    
    # 总结
    print_header("测试结果")
    print(f"配置验证: {'✅ 通过' if config else '❌ 失败'}")
    print(f"SMTP 测试: {'✅ 通过' if smtp_ok else '❌ 失败'}")
    
    if any(q.get('server_chan', {}).get('enabled') for q in config['queries']):
        print(f"Server酱 测试: {'✅ 通过' if server_chan_ok else '❌ 失败'}")
    
    if config and smtp_ok:
        print_success("\n所有测试通过！配置可以使用。")
        return 0
    else:
        print_error("\n部分测试失败，请检查配置。")
        return 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n")
        print_info("用户中断")
        sys.exit(130)
    except Exception as e:
        print_error(f"未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
