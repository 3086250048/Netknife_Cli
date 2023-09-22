from handler.var import State_Var,String_Var,Number_Var,List_Var,Inner_Var,Extend_Var
from netknife_ply import init_state as init
from netknife_ply import ssh_send_state as ssh_send

from ipaddress import ip_address



number_var=Number_Var()
str_var=String_Var()
list_var=List_Var()
states_var_1=State_Var(plys={'init':init,'ssh_send':ssh_send},current_state='init',prompts={'init':'#','ssh_send':'>'})
states_var_2=State_Var(plys={'init':init,'ssh_send':ssh_send},current_state='init',prompts={'init':'#','ssh_send':'>'})

inner_var=Inner_Var()

number_var.port=1
print(number_var.port)
number_var.retry=1
print(number_var.retry)
number_var.timeout=1
print(number_var.timeout)
number_var.timeout=1
print(number_var.timeout)

str_var.address='1.1.1.1'
print(str_var.address)
str_var.flag='openclose'
print(str_var.flag)
str_var.user='czz'
print(str_var.user)
str_var.pwd='wsajda'
print(str_var.pwd)
str_var.sort='forward'
print(str_var.sort)

list_var.addresses=['1.1.1.1','2.2.2.2']
print(list_var.addresses)
list_var.ports=[1,2,1]
print(list_var.ports)
states_var_1.ply='ssh_send'
print(states_var_2.ply)



inner_var.tcping_open=[('1.1.1.1',22),('1.1.1.1',22),('1.1.1.1',22),('1.1.1.1','1')]
inner_var.tcping_open_append(('2.2.2.2',223))
print(inner_var.tcping_open_pop())
print(inner_var.tcping_open)


ext_var=Extend_Var()

