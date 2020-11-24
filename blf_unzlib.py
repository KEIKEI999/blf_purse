import zlib
import sys


def blf_unzlib(inputBLF, outputBIN):
   # BLFの全データ取得
   f = open(inputBLF, 'rb')
   blf_data = f.read()
   f.close()
   
   # 解凍済みデータ保存先ファイル
   f2 = open(outputBIN, 'wb')
   
   offset = 0
   filesize = len(blf_data)
   decompress_data = b''
   compress_data = b''
   
   # 先頭ヘッダからサイズ抽出
   header_size = blf_data[4] + blf_data[5]*0x100
   offset += alignment_chk(header_size)
   
   cnt = 0  # 経過表示用カウンタ
   
   while True:
      if offset >= filesize:
         # offsetがデータ終端に到達
         break
      
      # zlibパッケージヘッダ抽出   
      obj_size = blf_data[offset+8] + blf_data[offset+9]*0x100 + blf_data[offset+10]*0x10000 + blf_data[offset+11]*0x1000000
      
      compress_data = blf_data[offset+0x20:offset+obj_size]
      decompress_data = zlib.decompress(compress_data)
      f2.write(decompress_data)
      
      offset += obj_size
      
      if offset+4 >= filesize:
         break;

      i = 0
      while True:
         tmp = str.format( "%c%c%c%c" % (blf_data[offset + i + 0], blf_data[offset + i + 1], blf_data[offset + i + 2], blf_data[offset + i + 3]) )
         if tmp == 'LOBJ':
            break
         elif i >= 4:
            print('LOBJ not found!')
            exit()
            break
         else:
            i += 1
      
      offset += i
      
      # 経過表示用
      if cnt % 100 == 0:
         print(offset)
      cnt += 1
   
   f2.close()

if __name__=='__main__':
   inputBLF = 'test.blf'
   outputBIN = 'test.bin'

   args = sys.argv
   
   # コマンドライン引数がある場合は、引数優先
   if len(args) >= 3:
      inputBLF = args[1]
      outputBIN = args[2]
   
   print("BLF=%s,output=%s" % (inputBLF,outputBIN))
   
   blf_unzlib(inputBLF,outputBIN)