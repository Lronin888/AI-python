from openai import OpenAI
from  netmiko import ConnectHandler
from docx import Document
import time
import os
from dotenv import load_dotenv
from ollama import Client
import time

load_dotenv(r'D:\AI+python\.env')
#巡检命令列表
commands = [
    'display version',
    'display clock',
    'display startup',
    'display license',
    'display device',
    'display power',
    'display fan',
    'display temperature all',
    'display cpu-usage',
    'display memory-usage',
    'display interface brief',
    'display traffic',
    'display current-configuration',
    'display logbuffer',
    'display trapbuffer',
    'display alarm all',
    'display vlan',
    'display ip routing-table',
    'display stp brief',
    'display lldp neighbor brief',
    'display ssh server status',
    'display acl all',
    'dir flash:',
    'display transceiver verbose'
]
#调用API接口
def AI_V3(data,ipadd):
  client = OpenAI(
      base_url='https://ark.cn-beijing.volces.com/api/v3',
      api_key=os.getenv("ARK_API_KEY"),

  )
  prompt = '''
      你是一名拥有CCIE/HCIE/H3CSE认证的高级网络工程师，擅长解析网络设备配置，能够根据用户给出的设备配置完成以下任务：
      1.准确识别用户提供的配置命令类型（思科/华三/华为）
      2.分析配置中的关键参数，并在文档中输出（包括但不限于VLAN、路由协议、ACL规则等）
      明白你的身份后，回复1
  '''
  stream = client.chat.completions.create(
      model="ep-m-20250228165213-cct67",
      messages=[
          {"role": "system", "content": prompt},
          {"role": "user", "content": data},
      ],
      stream=True,
  )
  filename = f'{dir_url}\%s' % ipadd + '.md'
  for chunk in stream:
      if not chunk.choices:
          continue
      print(chunk.choices[0].delta.content, end="",
      file=open(f'{filename}','a'))
  return filename

#调用本地大模型处理
def local_ollama(data,ipadd):
    ''' 
    本地模型最好使用32B或以上，32B以下模型效果较差
    '''
    client = Client(host='http://localhost:11434')
    text= '''
      你是一名拥有CCIE/HCIE/H3CSE认证的高级网络工程师，擅长解析网络设备配置，能够根据用户给出的设备配置完成以下任务：
      1.准确识别用户提供的配置命令类型（思科/华三/华为）
      2.分析配置中的关键参数，并在文档中输出（包括但不限于VLAN、路由协议、ACL规则等）
      明白你的身份后，回复1
  '''
    response_stream = client.generate(
        model='qwen:1.8b',
        system=text,
        prompt=data,
        options={
            'temperature': 1,
        },
        stream=True  
    )
    try:
        filename = f'{dir_url}\%s' % ipadd + '.md'
        for chunk in response_stream:
            print(chunk['response'], end='',flush=True,
            file=open(f'{filename}', 'a'))
            time.sleep(0.02)
        return filename
    except KeyboardInterrupt:
        print("\n用户中断了生成")
    except Exception as e:
        print(f"\n生成异常: {str(e)}")

def inspect_device(ip_address):
    device = {
        'device_type': 'huawei',
        'ip': ip_address,
        'username': 'ssh',
        'password': 'admin@123',
    }
    try:
        with ConnectHandler(**device) as conn:
            conn.enable()
            
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"{dir_url}\inspection_report_{ip_address}_{timestamp}.txt"
            
            with open(filename, 'w') as report:
                report.write(f"=== 交换机巡检报告 - {ip_address} ===\n")
                report.write(f"巡检时间：{time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                for cmd in commands:
                    output = conn.send_command(cmd, delay_factor=2)
                    report.write(f"[{cmd}] 输出：\n")
                    report.write("-"*60 + "\n")
                    report.write(output + "\n\n")

                    print(f"{ip_address} 成功执行：{cmd}")
            
            return filename
            
    except Exception as e:
        print(f"{ip_address} 连接失败：{str(e)}")
        return None

def main():
    dir_url = r"D:\AI+python\巡检报告"
    devices = [f'192.168.56.{sw}' for sw in range(10, 14)]
    for ip in devices:
        print(f"\n开始巡检设备 {ip}")
        report_file = inspect_device(ip)
        time.sleep(2)
        with open(f'{report_file}','r') as f:
            check_file = f.read()
            Report = AI_V3(check_file, ip)
            #Report = local_ollama(check_file, ip)
            time.sleep(2)
            if report_file:
                print(f"巡检报告已生成：{Report}")
        os.remove(report_file)
        print("-"*60)

if __name__ == '__main__':
    main()
