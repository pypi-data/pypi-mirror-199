import os,sys
from PIL import Image
from PIL import ImageTk
import tkinter.font, tkinter.ttk
import tkinter as tk
from tkinter import scrolledtext,constants
from datetime import datetime
import threading
import cv2
import traceback
import time 
from ftplib import FTP
import configparser
import logging
import asyncio
import numpy as np
from gps import *
# import winsdk.windows.devices.geolocation as wdg

class Fk_viewer(object):
    
    def __init__(self,env):
        
        logging.basicConfig(filename="recoding_file/em.log",filemode='a',
                            level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt="%m/%d/%Y %I:%M:%S %p %Z")
        self.env=env.upper()
        self.config = configparser.ConfigParser()
        self.config.read('./config.ini')
        self.window = tk.Tk() 
        self.window.geometry(self.config[self.env]['GEOMETRY'])
        self.window.attributes("-fullscreen", True)
        self.window.bind("<F11>", lambda event: self.window.attributes("-fullscreen",
                                    not self.window.attributes("-fullscreen")))
        self.window.bind("<Escape>", lambda event: self.window.attributes("-fullscreen", False))
        self.window.title("EM_transfer:Suncom Co.,Ltd.")
        self.img= ImageTk.PhotoImage(Image.open("img/background.jpg"))
        self.back_g=tk.Canvas(self.window,height=720, width=1280)
        self.back_g.create_image(0,0, image=self.img,anchor="nw")
 
        self.vessel_name=self.config[self.env]['VESSEL_NAME']
        self.path=self.config[self.env]['PATH']
        self.target_path=self.config[self.env]['TARGET_PATH']
        try:
            if self.env=="DEFAULT":
                self.view = cv2.VideoCapture(int(self.config[self.env]['VIDEOCAPTURE']))
            else:
                self.view = cv2.VideoCapture(self.config[self.env]['VIDEOCAPTURE'])
        except cv2.error as ex:
            logging.error(ex)
            time.sleep(5)
        w = round(self.view.get(cv2.CAP_PROP_FRAME_WIDTH)) # width
        h = round(self.view.get(cv2.CAP_PROP_FRAME_HEIGHT)) #height
        fps = self.view.get(cv2.CAP_PROP_FPS) #frame per second
        logging.info(f"Checking... for receivied IP camera info to being: ,{w},{h},{fps}")
        self.txt_idx=1
        # # self.image=np.array([])
        self.out=None
        self.t_img=None
        self.thread_seq=None
        self.thread_time=None
        self.thread_file_trans=None
        self.thread_gps=None
        self.file_exist=False
        self.out_set=None
        self.num=0
        # self.lastShownPercent=0

        self.entryText1 = tk.StringVar() 
        self.entryText2 = tk.StringVar()
        self.entryText3 = tk.StringVar()
        self.entryText4 = tk.StringVar()
        self.entryText5 = tk.StringVar()

        
        lfont = tkinter.font.Font(family="맑은 고딕", size=18 , weight = "bold")
        lfont1 = tkinter.font.Font(family="맑은 고딕", size=25 , weight = "bold")
        lfont2 = tkinter.font.Font(family="맑은 고딕", size=16 , weight = "bold")
        self.cur_time = tk.Entry(self.back_g, textvariable = self.entryText1,
                                 width=10,font=lfont,bd=0,foreground="white",background="black"
                                 ,highlightthickness=0)
        aa =self.back_g.create_window(1060,162,window=self.cur_time)
        self.cur_time2 = tk.Entry(self.back_g, textvariable = self.entryText2
                                  ,width=7,font=lfont,bg='black',bd=0,foreground="white"
                                  ,highlightthickness=0)
        aa =self.back_g.create_window(1060,208,window=self.cur_time2)
        self.cur_time3 = tk.Entry(self.back_g, textvariable = self.entryText3,
                                  width=13,font=lfont1,bg='black',bd=0,foreground="white"
                                  ,highlightthickness=0)
        aa =self.back_g.create_window(1050,367,window=self.cur_time3)
        self.entryText3.set(self.vessel_name)
        self.cur_time4 = tk.Entry(self.back_g, textvariable = self.entryText4,
                                  width=15,font=lfont,bg='black',bd=0,foreground="white"
                                  ,highlightthickness=0)
        aa =self.back_g.create_window(1060,483,window=self.cur_time4)
        self.entryText4.set("lat")
        self.cur_time5 = tk.Entry(self.back_g, textvariable = self.entryText5,
                                  width=15,font=lfont,bg='black',bd=0,foreground="white"
                                  ,highlightthickness=0)
        aa =self.back_g.create_window(1060,530,window=self.cur_time5)
        self.entryText5.set("lon")
        # self.entryText1.set('Recording does not start')
        # self.f_name = tk.Entry(frame2, textvariable = self.entryText2,width=30,font=lfont)
        # self.entryText2.set('Recording does not start')

        self.img_on = ImageTk.PhotoImage(Image.open("img/button_recoding.jpg"))
        self.img_off = ImageTk.PhotoImage(Image.open("img/button_recoding2.jpg"))
        self.img_on1 = ImageTk.PhotoImage(Image.open("img/button_stopping.jpg"))
        self.img_off1 = ImageTk.PhotoImage(Image.open("img/button_stopping2.jpg"))
        
        self.startingbtn = tk.Button(self.back_g, width=330,height=140, font=lfont2,text = "녹화시작",
                                     command = self.Mouse_event,
                                     image=self.img_on,relief='flat',bd=0,highlightthickness=0) 
        aa =self.back_g.create_window(240,685,window=self.startingbtn)
        
        self.exe_text = scrolledtext.ScrolledText(master=self.back_g,width=57,height=3) 
        self.exe_text.config(fg="white",bg="black",highlightthickness=0,bd=0)
        aa =self.back_g.create_window(1025,645,window=self.exe_text)
        
        self.trans_text = scrolledtext.ScrolledText(master=self.back_g,width=57,height=3) 
        self.trans_text.config(fg="white",bg="black",highlightthickness=0,bd=0)
        aa =self.back_g.create_window(1025,720,window=self.trans_text)

        self.stopingbtn = tk.Button(self.back_g, width=330,height=140,font=lfont2,text = "녹화중지",
                               command = self.Mouse_event1,
                               image=self.img_off1,relief='flat',highlightthickness=0) 
        aa =self.back_g.create_window(600,685,window=self.stopingbtn)
        self.image_b = np.zeros((700,400))
        self.image_b = Image.fromarray(self.image_b)
        self.image_b = self.image_b.resize((700, 400))
        self.image_b = ImageTk.PhotoImage(self.image_b)
        self.label3 = tk.Label(self.back_g, foreground="red",font=lfont1,compound="center",bg="black",image=self.image_b)
        aa =self.back_g.create_window(420,335,window=self.label3)
        self.tt=True

        self.back_g.pack(expand=True, fill="both") #expand=YES, fill=BOTH)
        
        if self.thread_file_trans is None or not self.thread_file_trans.is_alive():
            self.thread_file_trans=threading.Thread(target=self.file_conveyance, args=())
            self.thread_file_trans.daemon=True
            self.thread_file_trans.start()
        if self.thread_gps is None or not self.thread_gps.is_alive():
            self.thread_gps=threading.Thread(target=self.gps_loop, args=())
            self.thread_gps.daemon=True
            self.thread_gps.start()
        if self.thread_time is None or not self.thread_time.is_alive():
            self.thread_time=threading.Thread(target=self.time_loop, args=())
            self.thread_time.daemon=True
            self.thread_time.start()
        self.startingbtn.invoke()
        self.window.mainloop()
        
    def Mouse_event(self):
        # if(self.startingbtn['bg']==self.colour_on):
        self.startingbtn.config(image=self.img_on)
        self.stopingbtn.config(image=self.img_off1)
        self.start_recoding()
        
    def Mouse_event1(self):
        # if(self.stopingbtn['bg']==self.colour_on):
        self.startingbtn.config(image=self.img_off)
        self.stopingbtn.config(image=self.img_on1)
        self.stop_recoding_btn()    
        
    def gps_loop(self):
        try:
            os.system("sudo systemctl restart gpsd")
            gpsd=gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
            print ("Application started!",gpsd)  
            aa=["0","0"]
            while True:
                if gpsd:
                    a=self.getPositionData(gpsd)
                    logging.info(f"{a}")
                    if a:
                        aa=a
                        self.entryText4.set(a[1])
                        self.entryText5.set(a[0])
                        time.sleep(1.0)
                    else:
                        self.entryText4.set(aa[1])
                        self.entryText5.set(aa[0])
                        time.sleep(1.0)
                else:
                    os.system("sudo systemctl restart gpsd")
                    a=self.getPositionData(gpsd)
                    if a:
                        aa=a
                        self.entryText4.set(a[1])
                        self.entryText5.set(a[0])
                        time.sleep(1.0)
                    else:
                        self.entryText4.set(aa[1])
                        self.entryText5.set(aa[0])
                        time.sleep(1.0)

        except (KeyboardInterrupt):
            running = False
            print ("Applications closed!")
            
    def getPositionData(self,gpsd):
        nx =gpsd.next()
        if nx['class'] == 'TPV':
            latitude = getattr(nx,'lat', "Unknown")
            longitude = getattr(nx,'lon', "Unknown")
            # print(str(longitude), str(latitude))
            return [str(longitude),str(latitude)]
    def time_loop(self):
        while True:
            d=datetime.utcnow()
            aa1= str(d).split(" ")
            # print(aa1)
            self.entryText1.set(aa1[0])
            self.entryText2.set(aa1[1])
            time.sleep(1)            
    def winclose(self):
        self.tt=False
        self.window.destroy()
  
    def start_recoding(self):
        # print("========")
        self.tt=True
        if self.thread_seq is None or not self.thread_seq.is_alive():
            self.thread_on=True
            self.out_set=True
            self.thread_seq=threading.Thread(target=self.start_recoding1, args=())
            # self.thread_seq.daemon=True
            self.thread_seq.start()
        
        if self.thread_file_trans is None or not self.thread_file_trans.is_alive():
            self.thread_file_trans=threading.Thread(target=self.file_conveyance, args=())
            # self.thread_file_trans.daemon=True
            self.thread_file_trans.start()

    def start_recoding1(self):
        ii=0
        while True:
            if self.out_set==False:
                break
            time.sleep(1)
            if self.thread_on==False:
                break
            if self.out is None or not self.out.isOpened():
                if self.t_img is None or not self.t_img.is_alive():
                    logging.info(f"cnt: {ii+1}")
                    try:
                        if not self.view.isOpened():
                            if self.env=="DEFAULT":
                                self.view = cv2.VideoCapture(0)
                            else:
                                self.view = cv2.VideoCapture(self.config[self.env]['VIDEOCAPTURE'])
                    except cv2.error as ex:
                        logging.error(f'Traceback error: {ex},{traceback.print_exc()}')
                        # traceback.print_exc()
                    self.t_img = threading.Thread(target=self.sample_viewThread, args=())
                    # self.t_img.daemon =True
                    self.t_img.start()
                                
    def sample_viewThread(self):
        #print("txt_dix: ",txt_idx)
        fr =[]
        idx=1
        mbyte_cnt=0
        snap_freq = int(self.config[self.env]['SNAP_FREQ'])
        setting_frame_cnt=int(self.config[self.env]['SETTING_FRAME_CNT'])
        (file_name, file_name_s,path_file_name,path_file_name_s)=self.setting_file_name()
        
        w = round(self.view.get(cv2.CAP_PROP_FRAME_WIDTH)) # width
        h = round(self.view.get(cv2.CAP_PROP_FRAME_HEIGHT)) #height
        if self.config[self.env]['FPS']=="AUTO":
            fps = self.view.get(cv2.CAP_PROP_FPS) #frame per second
        else: fps = int(self.config[self.env]['FPS_SET']) 
        codec_tmp=self.config[self.env]['CODEC']
        fourcc = cv2.VideoWriter_fourcc(*codec_tmp) #fourcc
        delay = round(1000/fps)
        logging.info(f"{file_name} Checking... for going to be saved file")
            
        if not self.view.isOpened() and not self.out.isOpened():
            logging.error("Check to IP camera states or File isn't opend!!")
            self.stop_recoding_btn()
        try:
            if self.out is None or not self.out.isOpened():
                if not self.out is None:
                    self.out.release()
                self.out = cv2.VideoWriter(
                    filename=path_file_name,
                    fourcc=fourcc,
                    # apiPreference=cv2.CAP_FFMPEG,
                    fps=float(fps),
                    frameSize=(w, h),
                    isColor=True)#path_file_name, fourcc, fps, (w,h))
                # logging.error(self.out.isOpened())
        except cv2.error as ex:
            logging.exception(f'Traceback error: {ex}, {traceback.print_exc()}')
            
        try:
            start = time.time()
            while True:
                
                ret, fr = self.view.read()
                if not ret:
                    fr=[]
                    self.view.release()
                    self.out.release()
                    break
                if ret and idx <=setting_frame_cnt and self.out_set==True:#self.out.isOpened():
                    mbyte_cnt+=sys.getsizeof(fr)
                    
                    self.update_progress(idx/setting_frame_cnt,file_name,self.exe_text)
                    
                    if self.out.isOpened():
                        self.out.write(fr)
                    else:
                        break
                    # if idx % snap_freq==0:
                    image = cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(image)
                    image = image.resize((700, 400))
                    image = ImageTk.PhotoImage(image)
                    # self.image=image
                    self.label3.config(text="녹화중...",bg="black")
                    self.label3.configure(image=image)
                    self.label3.image=image
                    
                    cv2.waitKey(delay=delay)
                    
                else:
                    self.stop_recoding(file_name,file_name_s,path_file_name,path_file_name_s)
                    file_size=(os.path.getsize(path_file_name_s))/1024/1024
                    
                    self.exe_text.insert("end", 
                                         f'\nThe file {file_name}({round(file_size,2)}MB) saved sucessfully\n')
                    end = time.time()
                    self.exe_text.insert("end",f"{file_name} it took {end - start:.5f} sec\n" )
                    self.exe_text.see("end")
                    logging.info(f'The file {file_name}({round(file_size,2)}MB) saved sucessfully')
                    
                    break
                idx+=1
        except(KeyboardInterrupt, SystemExit):
                logging.exception('Exit dut to keyboard interrupt')
        except Exception as ex:
            logging.exception(f'Traceback error: {ex}')
            traceback.print_exc()
        finally:
            #self.view.release()
            self.out.release()
            
    def setting_file_name(self):

        self.image=[]
        d=datetime.now()
        file_name= f"f{d.strftime('%Y%m%d%H%M%S')}{self.vessel_name}.mp4"
        file_name_s= f"fc{d.strftime('%Y%m%d%H%M%S')}{self.vessel_name}.mp4"
        path_file_name=os.path.join(self.path,file_name)
        path_file_name_s=os.path.join(self.path,file_name_s)
        # self.entryText2.set(file_name) 
        return file_name,file_name_s,path_file_name,path_file_name_s       
        
    def stop_recoding_btn(self):
        
        self.label3.config(text="녹화 중지됨 !",bg="black")
        self.label3.configure(image=self.image_b)#self.image)
        self.image=self.image_b
        self.thread_on=False
        self.out_set=False
        # self.out.release()
            
    def stop_recoding(self,file_name,file_name_s,path_file_name,path_file_name_s):

        self.out.release()
        self.label3.config(text="녹화 중지됨 !",bg="black")
        self.label3.configure(image=self.image_b)#self.image)
        self.image=self.image_b
        # self.label3.pack()
        if os.path.isfile(path_file_name):
            os.rename(path_file_name,path_file_name_s)
            
    def update_progress(self,progress,file_name,tk_text):
        barLength = 10 # Modify this to change the length of the progress bar
        status = ""
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
            status = "error: progress var must be float"
        if progress < 0:
            progress = 0
            status = "Halt..."
        if progress >= 1:
            progress = 1
            status = "Done..."
        block = int(round(barLength*progress))
        text = "{3} is [{0}] {1}% {2} ".format( "#"*block + "-"*(barLength-block),
                                                           round(progress*100,2), status,file_name)
        
        exe_idx = float(tk_text.index("insert"))
        
        aa = list(str(exe_idx).split('.'))
        if int(aa[1])>0:
            tk_text.delete(f"{aa[0]}.0",f"{aa[0]}.{int(aa[1])}")

        tk_text.insert("insert",text)
        tk_text.see("insert")

        # sys.stdout.flush()
        # return text
    
    def sumof_progress(self,block):
        print("==================shit")
        sizeWritten += 1024
        percentComplete = round((sizeWritten / self.totalSize) * 100)
        
        if (self.lastShownPercent != percentComplete):
            self.lastShownPercent = percentComplete
            print(str(percentComplete) + " percent complete")
            self.update_progress(percentComplete,self.file_tr_name,self.trans_text)

    def file_conveyance(self):
        
        while True:
            start = time.time()
            if self.tt==False:
                break
            try:
                time.sleep(1) #fc2023
                file_tmp=[f for (dirpath, dirnames, filenames) in os.walk(self.path) for f in filenames if "fc" in f]
                
                if len(file_tmp):
                    logging.info(f"file_name : {file_tmp} and cnt:{len(file_tmp)}")
                # if file_tmp:
                #     self.file_exist=True
                
                if len(file_tmp):#self.file_exist:
                    file_tr_name=file_tmp[0]
                    year_=file_tr_name[2:6]
                    month_=file_tr_name[6:8]
                    day_=file_tr_name[8:10]
                    file_path = os.path.join(self.path,file_tr_name)
                    total=os.path.getsize(file_path)
                    host=self.config[self.env]['FTP_SERVER_IP']
                    m_path=""
                    try:
                        
                    # with open(file_path ,mode='rb') as uploadfile:
                        with FTP(host) as session:
                            session.login(self.config[self.env]['FTP_ID'],
                                        self.config[self.env]['FTP_PASS'])
                            session.set_pasv(True)
                            session.cwd(self.target_path)
                            #----------------------------------------------------------------
                            y_=[h for h in session.nlst() if year_ in h]
                            # print(y_)
                            if not len(y_):
                                session.mkd(f"{self.target_path}/{year_}")
                                session.mkd(f"{self.target_path}/{year_}/{month_}")
                                session.mkd(f"{self.target_path}/{year_}/{month_}/{day_}")
                                m_path=f"{self.target_path}/{year_}/{month_}/{day_}"
                            else :
                                session.cwd(f"{self.target_path}/{year_}")
                                m_=[h for h in session.nlst() if month_ in h]
                                # print(m_)
                                if not len(m_):
                                    session.mkd(f"{self.target_path}/{year_}/{month_}")
                                    session.mkd(f"{self.target_path}/{year_}/{month_}/{day_}")
                                    m_path=f"{self.target_path}/{year_}/{month_}/{day_}"
                                else:
                                    session.cwd(f"{self.target_path}/{year_}/{month_}")
                                    d_=[h for h in session.nlst() if day_ in h]
                                    if not len(d_):
                                        session.mkd(f"{self.target_path}/{year_}/{month_}/{day_}")
                                        m_path=f"{self.target_path}/{year_}/{month_}/{day_}"
                                    else:
                                        session.cwd(f"{self.target_path}/{year_}/{month_}/{day_}")
                                        m_path=f"{self.target_path}/{year_}/{month_}/{day_}"    
                            #-----------------------------------------------------------------
                            # file_path = os.path.join(self.path,file_tr_name)
                            
                            
                            with open(file_path ,mode='rb') as uploadfile:
                                session.encoding='utf-8'
                                
                                # self._f_name=file_tr_name
                                totalSize=os.path.getsize(file_path)
                                uploadTracker=self.FtpUploadTracker(int(totalSize),file_tr_name)#,self.trans.text)
                                session.storbinary("STOR " + f"{m_path}/{file_tr_name}"
                                                   , uploadfile) #,1024 #, uploadTracker.handle)
                                                #    ,callback=uploadTracker.handle)

                                self.num=0
                                end = time.time()
                                self.trans_text.insert("end", f"{file_tr_name} ({round(total/1024/1024,2)}MB) was transfered successfully.\n")
                                self.trans_text.insert("end",f"{file_tr_name} it took {end - start:.5f} sec\n")
                                # self.trans_text.see("end")
                        try:
                            file= os.path.join(self.path,file_tr_name)
                            if os.path.isfile(file):
                                os.remove(file)
                                self.trans_text.see("end")
                                
                                # print(f"{end - start:.5f} sec")
                                logging.info(f"{file_tr_name} it took {end - start:.5f} sec")
                            else: pass
                        
                        except Exception as ex:
                            logging.exception(f'Traceback error: {ex}')
                            traceback.print_exc()
                    except(KeyboardInterrupt, SystemExit):
                        logging.exception('Exit dut to keyboard interrupt')
                    except Exception as ex:
                        logging.exception(f'Traceback error: {ex}')

            except(KeyboardInterrupt, SystemExit):
                    logging.exception('Exit dut to keyboard interrupt')
            except Exception as ex:
                logging.exception(f'Traceback error: {ex}')
                traceback.print_exc()
    class FtpUploadTracker:
        sizeWritten = 0
        totalSize = 0
        lastShownPercent = 0
        file_name=""
        trans_text_=None
        
        def __init__(self, totalSize,file_name):#,trans_text):
            self.totalSize = totalSize
            self.file_name = file_name
            # self.trans_text_=trans_text
        def handle(self, block):
            self.sizeWritten += 1024
            percentComplete = round((self.sizeWritten / self.totalSize) * 100)
            
            if (self.lastShownPercent != percentComplete):
                self.lastShownPercent = percentComplete
                print(str(percentComplete) + " percent complete")           
                # Fk_viewer.update_progress(percentComplete,self.file_name,self.trans_text)

if __name__ == "__main__":
    env = sys.argv[1] if len(sys.argv) >= 2 else "DEFAULT"
    t = Fk_viewer(env)

