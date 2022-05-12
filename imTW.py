# -*- coding: UTF-8 -*-
#=============================================================================
# zuo,Feb 15, 2022
# imTW.py # improved TW calculate
#=============================================================================
import math,sys
def calEw(T_C):
# T_C ：输入，温度(摄氏度)
# 通过【纯水平液面饱和水汽压采用世界气象组织(WMO)推荐的戈夫-格雷奇(Goff-Gratch)公式】
# 计算纯水平液面饱和水汽压E_w
	T1=273.16
	T=T_C+273.15

	if T_C>0:
		logE_w=10.79574*(1-T1/T)-5.028*math.log(T/T1)+ \
				1.50475*(10E-4)*(1-math.pow(10,(-8.2969*(T/T1-1))))+ \
				0.42873*(10E-3)*(math.pow(10,(4.76955*(1-T1/T)))-1)+0.78614
		return math.pow(10,logE_w)
	else:
		logE_i=-9.09685*(T1/T-1)-3.56654*math.log(T1/T)+ \
				0.87682*(1-T/T1)+0.78614
		return math.pow(10,logE_i)

def guessTw(T_dry,P,rh,Tw):
#给定：E_w   ：湿球温度Tw所对应的纯平面液面饱和水汽压
#      P     ：本站气压(hPa)
#      Tdry  ：干球温度(摄氏度)
#      T_w   ：湿球温度(摄氏度)，初值
#可根据公式$\tag C: t_{wet}=t_{dry}-[E_w(t_{wet})-\frac{rh*E_{w}(t_{dry})}{100}]*\frac{1}{AP}$求出对应的：
#输出        ：Tw_guess  ：湿球温度，猜测值
	A=(8.15E-4 if Tw>=0 else 7.19E-4)           #柱状，0.4m/s，#A=8.57E-4 #A=7.947E-4
	#A=(8.57E-4 if Tw>=0 else 7.56E-4)          #球状，0.4m/s，#A=8.57E-4 #A=7.947E-4
	A=7.947E-4                                 #现用，0.8m/s，如果是分段函数有可能发生不收敛的情况，这时需要转为二分法，见下面的实现
	t_wet=T_dry-(calEw(Tw)-rh*calEw(T_dry)/(100))/(A*P) # print("guessTw:",[T_dry,P,rh,Tw,A*P],"t_wet:",t_wet)
	return t_wet

def calTw(T,P,RH):
	[ESP,Xi,LOOPCOUNT]=[10, T-10, 0]
	while LOOPCOUNT<20:
		LOOPCOUNT=LOOPCOUNT+1
		u=guessTw(T,P,RH,Xi);
		v=guessTw(T,P,RH,u);
		#Xi=( v-(v-u)**2/(v-2*u+Xi) if 1e-2<abs(v-2*u+Xi) else u)
		Xi=( v-(v-u)**2/(v-2*u+Xi) )
		#ESP=abs(Xi-xn) #用这个当作误差指标是比较合理的
		ESP=abs(u-v) #用这个当作误差指标是比较合理的
		#print(LOOPCOUNT,ESP,u,v,"Xi=",Xi)
		if ESP<0.01:break 
	if ESP>0.01:print("ESP>1e-3, move to binary")
	[LOOPCOUNT,u,v]=[0,Xi+1,Xi-1]
	while ESP>0.01:
		LOOPCOUNT=LOOPCOUNT+1
		if LOOPCOUNT>20:
			print("BINARY Cannot get the value:",[T,P,RH])
			break;
		#Xi=guessTw(T,P,RH,(u+v)/2)
		#print("T Binary:,u,v,?",u,v,Xi,u>v)
		Xi=(u+v)/2 #
		ESP=Xi-guessTw(T,P,RH,Xi)
		if (ESP>0):
			u=Xi
		else:
			v=Xi
		ESP=abs(ESP)
	#print("LOOP :",LOOPCOUNT,"ESP,u,v,Xi:",ESP,u,v,Xi) #print("final: ",Xi,guessTw(T,P,RH,Xi))
	return Xi


if __name__=="__main__":

	if 2!=len(sys.argv[1:]):
		print("usage: "+sys.argv[0]+' inputfile'+' outputfile')
		sys.exit()
	else:
		[infile,outfile] =[sys.argv[1],sys.argv[2]]
	[debugcounter,debugMaxLine]=[0,48203850] #注意这里是输入数据文件 ./AC-1951-2020_HOUR.TXT 的总行数
#	[debugcounter,debugMaxLine]=[0,8151]
	with open (outfile, "w") as fh_out: #with open ("./AC-1951-2020_HOUR_TW.TXT", "w") as fh_out:
		fh_out.writelines("{:6s}\t{:4s}\t{:2s}\t{:2s}\t{:2s}\t{:6s}\t{:6s}\t{:6s}\t{:9s}\n".format("STATIONNO","YEAR","MONTH","DAY","HOUR","TEMPERATURE","RHU","PRESSURE","TWET(AK)"))
		with open (infile, "r") as fh_in: #with open ("./AC-1951-2020_HOUR.TXT", "r") as fh_in:
			line = fh_in.readline()
			for line in fh_in:
				fields=line.strip().split() #print(fields) #print(all(item.replace('.','',1).replace('-','',1).isdigit() for item in fields)) #				print([item.isdigit() for item in fields])
				if 8==len(fields) and all(item.replace('.','',1).replace('-','',1).isdigit() for item in fields): # must be 8 fields!
					[T,RH,P]=[float(fields[i]) for i in [5,6,7]] #					print(debugcounter,T,T>-100,T<100,RH,RH>=0,RH<=100,P,P>500,P<1200)
					if 100.0>T and -100<T and 0<=RH and 100>=RH and 500<P and 1200>P:
						#print("LINE:{:9d}\t{:6s}\t{:4s}\t{:2s}\t{:2s}\t{:2s}\t{:6s}\t{:6s}\t{:6s}\t{:4.1f}".format(debugcounter,fields[0],fields[1],fields[2],fields[3],fields[4],fields[5],fields[6],fields[7],calTw(T,P,RH)))
						finalTW=calTw(T,P,RH)
						if(-100>finalTW):
							print(">20 Times at LINE:",debugcounter,":",line)
						# 0.1 is ok for realneed: fh_out.writelines("{:6s}\t{:4s}\t{:2s}\t{:2s}\t{:2s}\t{:6s}\t{:6s}\t{:6s}\t{:9.5f}\n".format(fields[0],fields[1],fields[2],fields[3],fields[4],fields[5],fields[6],fields[7],finalTW))
						fh_out.writelines("{:6s}\t{:4s}\t{:2s}\t{:2s}\t{:2s}\t{:6s}\t{:6s}\t{:6s}\t{:6.1f}\n".format(fields[0],fields[1],fields[2],fields[3],fields[4],fields[5],fields[6],fields[7],finalTW))
					else:
						print('invalid float:[T,RH,P]=',[T,RH,P])
				if debugcounter>=debugMaxLine:
					break
				debugcounter=debugcounter+1

