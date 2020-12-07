import re

from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin


app = Flask(__name__)

registerdict = {
            '$t0': '01000',
            '$t1': '01001',
            '$t2': '01010',
            '$t3': '01011',
            '$t4': '01100',
            '$t5': '01101',
            '$t6': '01110',
            '$t7': '01111',
            '$s0': '10000',
            '$s1': '10001',
            '$s2': '10010',
            '$s3': '10011',
            '$s4': '10100',
            '$s5': '10101',
            '$s6': '10110',
            '$s7': '10111',
            '$t8': '11000',
            '$t9': '11001',
}


opcode = {
    'add': '000000',
    'and': '000000',
    'addu': '000000',
    'addiu': '001001',
    'nor': '000000',
    'sub': '000000',
    'addi': '001000',
    'andi': '001100',
    'lw': '100011', 
    'sw': '101011',
    'sll': '000000', 
    'j': '000010', 
    'bne': '000101',
    'beq': '000100'
}


# 'add','and',    'addu'    'addiu'    'nor'   'sub' 'addi' 'andi' 'lw' 'sw' 'sll' 'j'
    
funcode = {
    'add': '100000',   
    'and': '100100',
    'addu': '100001',
    'nor': '100111',
    'sub': '100010',
    'sll': '000000'
    }




class Converter:
    def __init__(self,request):
        self.request = request

    def check_type(self):
        ret_data = {'result': '', 'value': '', 'type': ''}
        lines = request.args.get('initval')
        init_type = request.args.get('type')
        print(lines, init_type)
        if init_type == 'binary':
             ret_data = self.check_data_Validity_bin(lines)
        else:
             ret_data = self.check_data_Validity_mips(lines)
        return ret_data


    def check_data_Validity_bin(self, lines):

        ret_data = {'result': '', 'value': '', 'type': ''}
        
        bin_line = lines.replace(" ", "")
        

        binary = ""
        for i in(bin_line):
            if i in '10':
                binary = True
            else:
                binary =  False
                break
        if binary == False:
                ret_data['result'] = 'error'
                ret_data['value'] = 'Invalid Data'
                ret_data['type'] = ''
                    
        else:
            if len(bin_line) != 32:
                ret_data['result'] = 'error'
                ret_data['value'] = 'Length of binary must be 32'
                ret_data['type'] = ''
            else:
                op_bin = str(bin_line[:6])
                fun_code = ""
                operation = ''
                r1 = ""
                r2 = ""
                r3 = ""
                if op_bin in ['001000', '001001', '001100', '000100', '000101', '100011', '101011']:

                    for k, v in opcode.items():
                        if op_bin ==v:
                            fun_code = k
                        else:
                            continue
                    
                    for k, v in registerdict.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                        if v == bin_line[6:11]:
                                r1 = k
                        elif v == bin_line[11:16]:
                            r2 = k
                        
                        else:
                            continue
                        r3 = int(bin_line[-16:], 2)

                        if fun_code != "" and r1 != "" and r2 != "" and r3 != "":

                            ret_data['result'] = 'success'
                            if fun_code in ['lw', 'sw']:
                                ret_data['value'] = f'{fun_code}, {r2}, {str(r3)}({r1})'
                            else:
                                ret_data['value'] = f'{fun_code,} {r2}, {r1},  {str(r3)}'                        
                            ret_data['type'] = 'Integer Type'
                        else:
                            ret_data['result'] = 'error'
                            ret_data['value'] = 'Length of binary must be 32'
                            ret_data['type'] = ''
                elif op_bin in ['000010', '000101', '000100']:
                    fun_code = [k for k,v in opcode.items() if v == '000010']
                    
                    if op_bin == '000010':
                        
                        if len(fun_code) > 0:
                            ret_data['result'] = 'success'
                            ret_data['value'] = f'{fun_code[0]}, Loop'
                            ret_data['type'] = 'Integer Type'
                        else:
                            ret_data['result'] = 'error'
                            ret_data['value'] = 'Invalid Data'
                            ret_data['type'] = ''
                    else:
                        if len(fun_code) > 0:
                            for k, v in registerdict.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                                if v == bin_line[6:11]:
                                    r1 = k
                                elif v == bin_line[11:16]:
                                    r2 = k
                        
                                else:
                                    continue
                            r3 = 'Loop'

                            if fun_code != "" and r1 != "" and r2 != "" and r3 != "":
                                print('tt')
                                ret_data['result'] = 'success'
                                ret_data['value'] = f'{fun_code[0]}, {r2}, {r1}, {r3}'
                                                 
                                ret_data['type'] = 'Integer Type'
                        else:
                            ret_data['result'] = 'error'
                            ret_data['value'] = 'Length of binary must be 32'
                            ret_data['type'] = ''                       
                        

                else:
                    for ks, vs in funcode.items():
                        
                        if vs == bin_line[-6:]:
                            
                            fun_code = ks
                        else:
                            continue

                    for k, v in registerdict.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                        if v == bin_line[6:11]:
                            r1 = k
                        elif v == bin_line[11:16]:
                            r2 = k
                        else:
                            
                            if v == bin_line[16:21]:
                                r3 = k
                            else:
                                continue
                    if fun_code == 'sll':
                        r3 = int(bin_line[21:27], 2)
                        print(r3)
                    if fun_code != "" and r1 != "" and r2 != "" and r3 != "":
                        ret_data['result'] = 'success'
                        if fun_code == 'sll':
                            ret_data['value'] = f'{fun_code}, {r2}, {r1}, {r3}'
                        else:
                            ret_data['value'] = f'{fun_code}, {r3}, {r1}, {r2}'
                        ret_data['type'] = 'Register Type'
                    else:
                        ret_data['result'] = 'error'
                        ret_data['value'] = 'Length of binary must be 32'
                        ret_data['type'] = ''

            
        return ret_data


    def check_data_Validity_mips(self, lines):  

        ret_data = {'result': '', 'value': '', 'type': ''}
        op_code = ""
        fun_code = ""
        bin_equi = ''
        rs = ""
        rt = ""
        rd = ""

        if lines != "":
            split_code = re.split("\s|,", lines)
            split_code = [st for st in split_code if st != ""]
           
        else:
            ret_data['result'] = 'error'
            ret_data['value'] = 'Invalid Data'
            ret_data['type'] = ''

        
        if len(split_code) > 1:
            
            if split_code[0] in opcode:
                op_code = opcode[split_code[0]]
                if split_code[0] in ['add', 'sub', 'and', 'nor' ]: 
                    
                    if len(split_code) == 4:
                        isvalid = True
                        if split_code[0] in list(opcode.keys()) and split_code[0] in list(funcode.keys()):
                        
                            fun_code = funcode[split_code[0]]
                            bin_equi = bin_equi + opcode[split_code[0]]
                                
                            if split_code[1] != "" and  split_code[1] in list(registerdict.keys()):
                                rd =  registerdict[split_code[1]]
                            else:
                                isvalid = False

                            if split_code[2] != "" and  split_code[2] in list(registerdict.keys()):
                                rs =  registerdict[split_code[2]]
                            else:
                                isvalid = False

                            if split_code[3] != "" and  split_code[3] in list(registerdict.keys()):
                                rt =  registerdict[split_code[3]]
                            else:
                                isvalid = False
                            if isvalid == True:
                               bin_equi = bin_equi + ' ' + rs + ' ' + rt + ' ' + rd

                            else:
                                ret_data['result'] = 'error'
                                ret_data['value'] = 'Invalid Data'
                                ret_data['type'] = ''
 
                                
                        else:
                            ret_data['result'] = 'error'
                            ret_data['value'] = 'Invalid Data'
                            ret_data['type'] = ''

                        if  ret_data['result'] != 'error' and fun_code != "":
                            bin_equi = bin_equi + ' ' + fun_code
                            ret_data['result'] = 'success'
                            ret_data['value'] = bin_equi
                            ret_data['type'] = 'Register Type'
                    else:
                        ret_data['result'] = 'error'
                        ret_data['value'] = 'Invalid Data'
                        ret_data['type'] = ''

                elif  split_code[0] in ["sll", "addi", "andi"]:
                   
                    if len(split_code) == 4:
                        bin_equi = bin_equi + opcode[split_code[0]]

                        for rs in split_code[1:3]:
                            if rs in list(registerdict.keys()):
                                bin_equi = bin_equi + ' ' + registerdict[rs]
                            else:
                                ret_data['result'] = 'error'
                                ret_data['value'] = 'Invalid Data'
                                ret_data['type'] = ''
                                break
                        if ret_data['result'] != 'error':

                            ret_data['result'] = 'success'
                        
                            ret_data['value'] = bin_equi + " " + str(format(int(split_code[-1]), '016b'))
                            if split_code[0] == 'sll':
                                ret_data['type'] = 'Register Type'
                            else:
                                ret_data['type'] = 'Integer Type'
                        


                    else:
                        ret_data['result'] = 'error'
                        ret_data['value'] = 'Invalid Data'
                        ret_data['type'] = ''
                
                elif split_code[0] in ["lw", "sw"] :
                    imm = ""
                    split_imm = re.split("\s|,|\(|\)", lines)
                    split_imm = [i for i in split_imm if i != ""]
                   
                    if len(split_imm) == 4:
                        isvalid = True
                        if split_imm[0] in list(opcode.keys()) :
                        
                            bin_equi = bin_equi + opcode[split_imm[0]]
                                
                            if split_imm[1] != "" and  split_imm[1] in list(registerdict.keys()):
                                rt =  registerdict[split_imm[1]]
                               
                               
                            else:
                                
                                isvalid = False

                            try:
                                imm =  str(format(int(split_imm[2]), '016b'))
                                
                            except:
                                isvalid = False
                              

                            if split_imm[3] != "" and  split_imm[3] in list(registerdict.keys()):
                                
                                rs =  registerdict[split_imm[3]]
                            else:
                                isvalid = False
                            if isvalid == True:
                                bin_equi = bin_equi + ' ' + rs + ' ' + rt + ' ' + imm
                                ret_data['result'] = 'success'
                                ret_data['value'] = bin_equi 
                                ret_data['type'] = 'Integer Type'

                            else:
                                ret_data['result'] = 'error'
                                ret_data['value'] = 'Invalid Data'                             
                                ret_data['type'] = ''
                            

                    else:
                        ret_data['result'] = 'error'
                        ret_data['value'] = 'Invalid Data'
                        ret_data['type'] = ''


                 


            else:
                ret_data['result'] = 'error'
                ret_data['value'] = 'Invalid Data'
                ret_data['type'] = ''

        else:
            ret_data['result'] = 'error'
            ret_data['value'] = 'Invalid Data'
            ret_data['type'] = ''


        return ret_data


@app.route('/',  methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def product_info():
    conv =  Converter(request)
    ret_json = conv.check_type()
    return ret_json

if __name__ == '__main__':
    CORS(app, support_credentials=True)
    app.run(debug=True)

"""if type == "r" :
    split_code = re.split("\s|,", mipscode)
    #among r type instr sll is in a different format hence i used if-else comparison
    if split_code[0] == "sll":
        print("Function type: R-Type")
        print("Instruction form: opcode|  rs |  rt |  rd |shamt| funct")
        print(opcode.get(split_code[0], "Not present") + "00000"+ registerdict.get(split_code[2], "Not present") + registerdict.get(split_code[1], "Not present") + format(int(split_code[3]),'05b') + funcode.get(split_code[0], "Not present"))

    else:
        print("Function type: R-Type")
        print("Instruction format: opcode|  rs |  rt |  rd |shamt| funct")
        print(opcode.get(split_code[0],"Not present") + registerdict.get(split_code[2],"Not present") + registerdict.get(split_code[3],"Not present") + registerdict.get(split_code[1],"Not present") +"00000"+ funcode.get(split_code[0],"Not present"))

elif type == "i" :
    split_imm = re.split("\s|,|\(|\)", mipscode)
    if split_imm[0] == "lw" or split_imm[0] == "sw":
        print("Function type: I-Type")
        print("Instruction format: opcode| rs | rt | Constant or address(imm)")
        print(opcode.get(split_imm[0],"Not present ") + registerdict.get(split_imm[3],"Not Present") + registerdict.get(split_imm[1] , "Not present") + format(int(split_imm[2]),'016b'))
    elif split_imm[0] == "j":
        print("Function type: I-Type")
        print("Instruction format: opcode| rs | rt | Constant or address(imm)")
        print(opcode.get(split_imm[0],"Not present") + format(int(split_imm[1]),'026b'))

    else:
        print("Function type: I-Type")
        print("Instruction format: opcode| rs | rt | Constant or address(imm)")
        print(opcode.get(split_imm[0],"Not present ") + registerdict.get(split_imm[3],"Not Present") + registerdict.get(split_imm[1] , "Not present") + format(int(split_imm[2]),'016b'))
else :
    print("The MIPS code entered is not supported")"""

