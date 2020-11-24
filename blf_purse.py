import sys

def blf_purse_can(data):
   txt = ''
   mObjectTimeStamp = data[24] + data[25]*0x100 + data[26]*0x10000 + data[27]*0x1000000
   mDlc = data[35]
   mID = data[36] + data[37]*0x100 + data[38]*0x10000 + data[39]**0x1000000
   mData = data[40:48]
   
   txt += 'Time:'+ str.format('%.9f' % (mObjectTimeStamp*0.000000001) ) + ', '
   txt += 'CAN:' + str.format('%08X' % (mID) ) + ', '
   txt += 'DLC:' + str(mDlc) + ','
   
   txt += 'Data: '
   for d in mData:
      txt += str.format('%02X' % (d) ) + ' '
   txt += '\n'
   
   return txt

def blf_purse_ethernet(data):
   txt = ''
   mObjectTimeStamp = data[24] + data[25]*0x100 + data[26]*0x10000 + data[27]*0x1000000
   mHardwareChannel = data[38] + data[39]*0x100
   mFramelength = data[54] + data[55]*0x100
   mData = data[64:64+mFramelength]
   
   txt += 'Time:' + str.format('%.9f' % (mObjectTimeStamp*0.000000001) ) + ', '
   txt += 'ETH:' + str.format('%08X' % (mHardwareChannel) ) + ', '
   txt += 'LEN:' + str(mFramelength) + ', '
   
   txt += 'Data: '
   for d in mData:
      txt += str.format('%02X' % (d) ) + ' '
   txt += '\n'
   
   return txt

def blf_purse(inputBIN, outputTXT):
   # BINの全データ取得
   f = open(inputBIN, 'rb')
   bin_data = f.read()
   f.close()
   
   filesize = len(bin_data)
   print('filesize=%x' % (filesize))
   # 解凍済みデータ保存先ファイル
   f2 = open(outputTXT, 'w')
   
   offset = 0;
   cnt = 0;
   
   while True:
      if offset >= filesize:
         break;
      
      txt = ''
      
      # オブジェクトサイズ取得
      obj_size = bin_data[offset+8] + bin_data[offset+9]*0x100 + bin_data[offset+10]*0x10000 + bin_data[offset+11]*0x1000000
      # オブジェクトタイプチェック
      mObjectType = bin_data[offset+0x0C] +  bin_data[offset+0x0D]*0x100 +  bin_data[offset+0x0E]*0x10000 +  bin_data[offset+0x0F]*0x1000000
      
      if mObjectType == 0x56:
         # CAN
         #print('can offset=%x' % (offset))
         txt = blf_purse_can(bin_data[offset:offset+obj_size])
         
      elif mObjectType == 0x78:
         # Ethernet
         #print('Ethernet offset=%x' % (offset))
         txt = blf_purse_ethernet(bin_data[offset:offset+obj_size])
         
      f2.write(txt)
      
      offset += obj_size
      
      if offset+4 >= filesize:
         break;

      i = 0
      while True:
         tmp = str.format( "%c%c%c%c" % (bin_data[offset + i + 0], bin_data[offset + i + 1], bin_data[offset + i + 2], bin_data[offset + i + 3]) )
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
      if cnt % 10000 == 0:
         print(offset)
      cnt += 1
      
   f2.close()


if __name__=='__main__':
   inputBIN = 'test.bin'
   outputTXT = 'test.txt'

   args = sys.argv
   
   # コマンドライン引数がある場合は、引数優先
   if len(args) >= 3:
      inputBIN = args[1]
      outputTXT = args[2]
   
   print("BIN=%s,TXT=%s" % (inputBIN,outputTXT))
   
   blf_purse(inputBIN, outputTXT)