import json
import os
import requests
from subprocess import check_output, Popen, PIPE
import signal
import getpass


class AIRPALibrary:
    def __init__(self):
        self.proses = True
        self.runner = None
        self.message = 'True'
        pass
    
    def start_timeout(self, seconds='10', process_name='IEDriverServer.exe'):
        '''Fungsi untuk menjalankan timeout dengan input yaitu berapa lama timeout akan dilakukan, serta
        proses apa yang ingin dimatikan
        
        Contoh penggunaan :

            Start Timeout    10    excel.exe
            Run Keyword And Ignore Error    Open Macro
            End Timeout
        '''
        self.initiate_timeout(True)
        self.timeout_process(seconds,process_name)
        
    def end_timeout(self):
        '''Fungsi untuk mendapatkan keterangan dari timeout yang dilakukan apakah berhasil atau tidaknyanya proses
        dijalankan dalam kurun waktu tertentu'''
        self.initiate_timeout(False)
        self.get_timeout_info()
    
    def get_timeout_info(self):
        if self.proses :
            if self.runner.communicate()[0].strip().decode('utf-8')[-5:].strip()=='True':
                raise RuntimeError('The execution failed because of time exceeded')
            else :
                print('Execution sucessfully initiated')
        else :
            if self.message=='True' :
                raise RuntimeError('The execution failed because of time exceeded')
            else :
                print('Execution sucessfully initiated')
    
    def initiate_timeout(self, set=True):
        if set:
            self.proses = set
        else :
            self.proses = set
            try :
                value = Popen("Taskkill /F /T /PID %d " % self.runner.pid+' /FI "USERNAME eq '+getpass.getuser(), stdout=PIPE)
                value = value.communicate()[0].strip().decode('utf-8').strip()
                if value!='INFO: No tasks running with the specified criteria.':
                    self.message = 'False'
            except :
                pass
                    
    def kill_process(self, process_name='excel.exe'):
        os.system('taskkill /F /IM '+process_name+' /FI "USERNAME eq '+getpass.getuser())
    
    def read_config(self,additional=None):
        ''' fungsi untuk membaca file konfigurasi json, pengguna dapat menambahkan untuk data 
            yang dibutuhkan dengan format json object. Output dari fungsi ini adalah file konfigurasi
            dalam bentuk json object.
            
            contoh penggunaan :
                ${config}=  read_config
            
        '''
        try:
            with open(os.getcwd()+'\\config.json') as jsonfile:
                conf = json.load(jsonfile)
        except:
            raise RuntimeError('File config.json tidak ditemukan')
        
        if additional!=None:
            try:
                conf.update(json.loads(additional))
            except:
                raise RuntimeError('Pastikan kembali json object yang dimasukkan sebagai parameter')
        return conf
    
    def timeout_process(self, seconds='10', process_name='IEDriverServer.exe'):
        if self.proses :
            self.runner = Popen(["python", os.path.dirname(os.path.realpath(__file__))+'\\function_timeout_robot.py',seconds,process_name], stdout=PIPE)
        else :
            value = Popen("Taskkill /F /T /PID %d " % self.runner.pid+' /FI "USERNAME eq '+getpass.getuser(), stdout=PIPE)
            value = value.communicate()[0].strip().decode('utf-8').strip()
            self.message = (value!='INFO: No tasks running with the specified criteria.')
            
    
    def timeout(self, function_module=None, seconds='10', process_name='excel.exe'):
        ''' Fungsi untuk menjalankan fungsi pada module dengan tambahan waktu timeout, fungsi ini memiliki parameter default kill process "excel.exe" dan timeout selama 10 detik
            
            Contoh Penggunaan :
                Timeout     [module].[fungsi]\n
                Timeout     [module].[fungsi]   30\n
                Timeout     [module].[fungsi]   30      apps.exe\n
                '''
        if function_module==None:
            raise RuntimeError('Please specify the module that need to be executed')
        
        value = check_output(["python", os.path.dirname(os.path.realpath(__file__))+'\\function_timeout.py',seconds,function_module,process_name])
        
        if bool(value.strip()[-5:].decode('utf-8'))==True:
            raise RuntimeError('The execution failed because of time exceeded')
        else :
            print('Execution sucessfully initiated')
            
    
    def send_email(self, subject=None, content=None, to=None, cc=None, file_path=None):
        ''' Fungsi untuk mengirimkan email dengan parameter input sebagai berikut ini :\n
            subject = (string) masukkan subject yang anda inginkan, contoh : RPA Email\n
            content = (string) masukkan content email atau isi dari email. content email bisa juga dengan menggunakan html layouting\n
            Untuk masukkan data receiver email baik to maupun cc bisa tunggal(string or list) atau banyak(list). Contoh adalah sebagai berikut : \n
            tunggal :
                to = 'example@contoh.com'   atau    to = ['example@contoh.com']\n
                cc = 'example@contoh.com'   atau    cc = ['example@contoh.com']
            banyak :
                to = ['example1@contoh.com','example2@contoh.com']\n
                cc = ['example1@contoh.com','example2@contoh.com']
                
            Untuk masukkan file path harus menggunakan full path file dan bisa tunggal(string or list) atau banyak(list). Contoh adalah sebagai berikut : \n
            tunggal :
                file_path = 'C://Dir//filename.exentension'   atau    file_path = ['C://Dir//filename.exentension']
            banyak :
                file_path = ['C://Dir//filename1.exentension','C://Dir//filename2.exentension']
                
            Contoh penggunaan dalam robot framework :
                Send Email    Isi Subject    Isi Content Message    example@contoh.com    ${None}    C:\\Doc\\filename.xls\n
                Send Email    Isi Subject    Isi Content Message    ${list_email}    ${None}    C:\\Doc\\filename.xls\n
                Send Email    Isi Subject    Isi Content Message    ${list_email}    ${None}    ${full_path_file_list}    
            '''
        base_url = os.getenv("RPAEmailGateway")
        cli_code = os.getenv("RPAEmailGatewayCode")
        url = base_url+"/send_email"
        
        if subject==None or content==None or to==None:
            raise RuntimeError('Subject, content and receiver email must not be empty')
        
        if isinstance(to, list)==False : to = [to]
        
        payload={
                'to':';'.join(to),
                'subject': subject,
                'content': content}
        
        if cc!=None:
            if isinstance(cc, list)==False : cc = [cc]
            payload['cc'] = ';'.join(str(c) for c in cc)
        
        print(payload)

        headers = {
            'X-Client-Code':cli_code
        } 
        
        try:
            if file_path!=None:
                files = {}
                
                if isinstance(file_path, list)==False : file_path = [file_path]
            
                for i in range(len(file_path)):
                    index_file=f'file{i}:'
                    read_file=open(file_path[i], 'rb')
                    files[index_file] = read_file
                    
                response = requests.request("POST", url, headers=headers, data=payload, files=files)
            else :
                response = requests.request("POST", url, headers=headers, data=payload)  
            
            if 'error' in response.text:
                raise RuntimeError(response.text)
            else :
                print(response.text)
        except Exception as e:
            raise RuntimeError(e)
        
        
    