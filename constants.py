import idc
import idaapi

def save_hex_data(start_addr, end_addr, output_file):
    # 打开输出文件以写入数据
    with open(output_file, 'wb') as f:
        # 遍历地址范围中的每个字节并写入文件
        for ea in range(start_addr, end_addr):
            byte = idc.get_wide_byte(ea)
            f.write(byte.to_bytes(1, byteorder='little'))

# 设置地址范围和输出文件的路径
start_address = 0x1425F1D20  # 起始地址
end_address = 0x1427FB1B5    # 结束地址
output_file_path = 'Enterprisedata.hex'

# 调用保存函数
save_hex_data(start_address, end_address, output_file_path)
