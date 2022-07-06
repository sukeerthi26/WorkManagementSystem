from calendar import calendar
from functools import partial
from sqlite3 import Cursor
from traceback import print_list
from unittest import result
from PIL import ImageTk
import PIL.Image
from PIL import Image
from tkinter import*
import tkinter as tk
from tkinter import filedialog
import tkinter.font as font
from matplotlib.style import available
from numpy import record
from pyparsing import col
from tkcalendar import Calendar
import mysql.connector
from tkinter import ttk
import datetime as dt
from datetime import date 

connection = mysql.connector.connect(host='sukeerthis-MacBook-Air.local',
                                         database='SE7',
                                         user='Sukeerthi',
                                         password='Sukeerthi@26')





todays_date=dt.datetime.today()    
class work:

    def __init__(self,nofworkers,start_date,requirement,priority):
        self.status='not started'
        self.nofworkers=nofworkers
        self.start_date=start_date
        self.requirement=requirement
        self.priority=priority
    
    def edit_detailsofwork(self,duration):
        self.status='completed'
        self.duration=duration
        
    
    
def clicked_work():
    list = root.grid_slaves()
    i=0
    for l in list:
        if(i<=len(list)-5):
            l.destroy()
            i=i+1
    btn1 = Button(root, text = 'Add a work', bd = '5', command = clicked_addawork)
    btn1.grid(row=2,column=1)
    btn2 = Button(root, text = 'View-Edit details of a work', bd = '5', command = clicked_viewdetails_work)
    btn2.grid(row=3,column=1)
    
    

    
def clicked_addawork():
        list = root.grid_slaves()
        i=0
        for l in list:
            if(i<=len(list)-5):
                l.destroy()
                i=i+1
        label_ = Label(root, text = "Enter the details of the work")
        label_.grid(row=2,column=1)
        
        #nofworkers
        l1=Label(root,text='Number of workers')
        l1.grid(row=3,column=1)
        nofworkers_var=tk.StringVar()
        nofworkers_entry = tk.Entry(root,textvariable=nofworkers_var, font=('calibre',10,'normal'))
        nofworkers_entry.grid(row=3,column=2)
        
        
        #calender
        l2=Label(root,text='Start date')
        l2.grid(row=4,column=1)
        cal = Calendar(root, selectmode = 'day',year = 2020, month = 5,day = 22)
        cal.grid(row=5,column=1)
        date_var=tk.StringVar()
        date_entry = tk.Entry(root,textvariable=date_var ,font=('calibre',10,'normal'))
        date_entry.grid(row=4,column=2)
        
        
        def grad_date():
            date_var.set(cal.get_date())
        Button(root, text = "Set Date",command = grad_date).grid(row=6,column=1)
        
        
        
        #priority
        l4=Label(root,text='Priority')
        l4.grid(row=7,column=1)
        priority=tk.StringVar()
        priority_entry = tk.Entry(root,textvariable = priority, font=('calibre',10,'normal'))
        priority_entry.grid(row=7,column=2)
        
        #requirement
        l5=Label(root,text='Requirement')
        l5.grid(row=8,column=1)
        requirement=tk.StringVar()
        requirement_entry = tk.Entry(root,textvariable = requirement, font=('calibre',10,'normal'))
        requirement_entry.grid(row=8,column=2)
        
        def submit_addawork():
            print( "nofworkers_var.get()" + nofworkers_var.get()) 
            print("date_var:" +date_var.get())
            print("priority: "+priority.get())
            print("requirement:"+requirement.get())
            Submit['text']='Saved!'
            def change_phrase_submit():
                Submit['text']='Submit'
            Submit.after(3000,change_phrase_submit)
            
            nofworkers_var_value=int(nofworkers_var.get())
            mySql_insert_query = """INSERT INTO work( No_of_workers_req,Start_date,Requirement, Priority, Status,Duration) VALUES
                           ( %s, %s,%s, %s ,'Not Started',0) """
            record = (int(nofworkers_var.get()),date_var.get(),requirement.get(),int(priority.get()) )
            cursor = connection.cursor()
            cursor.execute(mySql_insert_query,record)
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into Laptop table")
            cursor.close()

            nofworkers_var.set("")
            date_var.set("")
            priority.set("")
            requirement.set("")
            
        Submit=Button(root, text = "Submit",command = submit_addawork)
        Submit.grid(row=9,column=1)
        
      

#def clear():
 #   list = root.grid_slaves()
  #  for l in list:
   #     l.destroy()
def clicked_viewdetails_work():
        list = root.grid_slaves()
        i=0
        for l in list:
            if(i<=len(list)-5):
                l.destroy()
                i=i+1
        
        cursor = connection.cursor()
        cursor.callproc('get_work')
        # print results
        Label(root, text = 'Id',bd=10).grid(row=3,column=0)
        Label(root, text = 'Number of workers req',bd=10).grid(row=3,column=1)
        Label(root, text = 'Start date',bd=10).grid(row=3,column=2)
        Label(root, text = 'Requirement',bd=10).grid(row=3,column=3)
        Label(root, text = 'Priority',bd=10).grid(row=3,column=4)
        Label(root, text = 'Status',bd=10).grid(row=3,column=5)
        Label(root, text = 'Duration',bd=10).grid(row=3,column=6)
        Label(root, text = 'Ids workers',bd=10).grid(row=3,column=7)
        Label(root, text = 'no of workers alloted',bd=10).grid(row=3,column=8)
        print("Printing laptop details")
        for result in cursor.stored_results():
            print(type(result))
            #print(result.fetchall())
            i=4
            Results_=result.fetchall()
            if(Results_==[]):
                    top= Toplevel(root)
                    top.title('Message')

                    Label(top, text = 'No works are added to the system!',bd=20).grid(row=1,column=1)
                    break
            for lists in Results_:
                print('lists is')
                print(lists)
                
                for j in range(len(lists)):
                    tempLabel=Label(root, text = lists[j],bd=20)
                    tempLabel.grid(row=i,column=j)
                    tempLabel.config( fg= "white")
                Button(root, text = "Edit",command=partial(editawork,lists[0]),bd=20).grid(row=i,column=9)
                i=i+1


        #nofworkers
         
def editawork(id):
        print("\nid is")
        print(id)
        list = root.grid_slaves()
        i=0
        for l in list:
            if(i<=len(list)-5):
                l.destroy()
                i=i+1
        
    #Id
        l0=Label(root,text='Id')
        l0.grid(row=3,column=1)
        Id_var=tk.StringVar()
        Id_entry = tk.Entry(root,textvariable=Id_var, font=('calibre',10,'normal'))
        Id_entry.grid(row=3,column=2)
    #nofworkers
        l1=Label(root,text='Number of workers')
        l1.grid(row=4,column=1)
        nofworkers_var=tk.StringVar()
        nofworkers_entry = tk.Entry(root,textvariable=nofworkers_var, font=('calibre',10,'normal'))
        nofworkers_entry.grid(row=4,column=2)
        
        
        #calender
        l2=Label(root,text='Start date')
        l2.grid(row=5,column=1)
        cal = Calendar(root, selectmode = 'day',year = 2022, month = 5,day = 22)
        cal.grid(row=6,column=1)
        date_var=tk.StringVar()
        date_entry = tk.Entry(root,textvariable=date_var ,font=('calibre',10,'normal'))
        date_entry.grid(row=5,column=2)
        
        
        def grad_date():
            date_var.set(cal.get_date())
        Button(root, text = "Set Date",command = grad_date).grid(row=7,column=1)
        
        
        
        #priority
        l4=Label(root,text='Priority')
        l4.grid(row=8,column=1)
        priority=tk.StringVar()
        priority_entry = tk.Entry(root,textvariable = priority, font=('calibre',10,'normal'))
        priority_entry.grid(row=8,column=2)
        
        #requirement
        l5=Label(root,text='Requirement')
        l5.grid(row=9,column=1)
        requirement=tk.StringVar()
        requirement_entry = tk.Entry(root,textvariable = requirement, font=('calibre',10,'normal'))
        requirement_entry.grid(row=9,column=2)
        
        #Status
        l6=Label(root,text='Status')
        l6.grid(row=10,column=1)
        status_var=tk.StringVar()
        status_entry = tk.Entry(root,textvariable = status_var, font=('calibre',10,'normal'))
        status_entry.grid(row=10,column=2)
        
        #Duration
        l7=Label(root,text='Duration')
        l7.grid(row=11,column=1)
        duration_var=tk.StringVar()
        duration_entry = tk.Entry(root,textvariable = duration_var, font=('calibre',10,'normal'))
        duration_entry.grid(row=11,column=2)
        
        
        #workers_allotted
        l8=Label(root,text='IDs of workers alloted')
        l8.grid(row=12,column=1)
        workers_allotted_var=tk.StringVar()
        workers_allotted_entry = tk.Entry(root,textvariable = workers_allotted_var, font=('calibre',10,'normal'))
        workers_allotted_entry.grid(row=12,column=2)
        
        #number_of_workers_allotted
        l9=Label(root,text='Number of workers alloted')
        l9.grid(row=13,column=1)
        nof_workers_alloted_var=tk.StringVar()
        nof_workers_alloted_entry = tk.Entry(root,textvariable = nof_workers_alloted_var, font=('calibre',10,'normal'))
        nof_workers_alloted_entry.grid(row=13,column=2)
        
        def submit_addawork(current_Status):
            print( "HERE.....nofworkers_var.get()" + nofworkers_var.get()) 
            print("date_var:" +date_var.get())
            print("priority: "+priority.get())
            print("requirement:"+requirement.get())
            print('current_Status'+current_Status)

            

            cursor = connection.cursor()
            mysql_update_query = """Update work set No_of_workers_req=%s, Start_date=%s, Requirement=%s, Priority=%s, Status=%s, Duration=%s  where Id =%s """
            record = (int(nofworkers_var.get()),date_var.get(),requirement.get(),int(priority.get()),status_var.get(),int(duration_var.get()),id )
            cursor.execute(mysql_update_query,record)
            connection.commit()
            
            if(current_Status.lower()!='completed' and status_var.get().lower()=='completed'):
                print('current_Status'+current_Status)
                ids_of_workers_list=workers_allotted_var.get().split(",")
                for i in range(len(ids_of_workers_list)):
                    mysql_update_worker_query = """Update worker set works_completed=%s, Availability=%s where Id =%s """
                    # getting works alloted ids
                    mysql_update_worker_1_query="""SELECT works_completed FROM worker WHERE id=%s"""
                    record_worker=(int(ids_of_workers_list[i]),)
                    cursor.execute(mysql_update_worker_1_query,record_worker)
                    result=cursor.fetchall()
                    for row in result:
                        works_completed_string=row[0]
                    if(works_completed_string==""):
                        works_completed_string=Id_var.get()
                    else:
                        works_completed_string=",".join([works_completed_string,Id_var.get()])
                    record=(works_completed_string,'1111',int(ids_of_workers_list[i]))
                    cursor.execute(mysql_update_worker_query,record)
                    connection.commit()
                    
            
            cursor.close()
            nofworkers_var.set("")
            date_var.set("")
            priority.set("")
            requirement.set("")
            status_var.set("")
            duration_var.set("")
            Id_var.set("")
            nof_workers_alloted_var.set("")
            workers_allotted_var.set("")
        
        
        cursor = connection.cursor()
        cursor.callproc('get_work')
        for result in cursor.stored_results():
            print(type(result))
            for lists in result.fetchall():
                print('size of tuple list')
                print(len(lists))
                print('tuple is ')
                print(lists)
                if(lists[0]==id):
                    print("inside if clause ")
                    Id_var.set(lists[0])
                    nofworkers_var.set(lists[1])
                    date_var.set(lists[2])
                    requirement.set(lists[3])
                    priority.set(lists[4])
                    status_var.set(lists[5])
                    duration_var.set(lists[6])
                    workers_allotted_var.set(lists[7])
                    nof_workers_alloted_var.set(lists[8])
                    print('\n\nlists[5] is'+lists[5])
                    current_Status=lists[5]
        
        Submit=Button(root, text = "Submit",command =partial(submit_addawork,current_Status))
        Submit.grid(row=15,column=1)
        cursor.close()   
        
        
         
        
                
        
             
class worker:
    def __init__(self,role,skill_level):
        self.role=role
        self.skill_level=skill_level
        self.availability='1111'
        self.nofhours_worked=0
        
    def edit_details(self,nofhours_worked,work_completed):
        self.nofhours_worked=nofhours_worked
        self.works_completed.append(work_completed)
        
def clicked_worker():
    list = root.grid_slaves()
    i=0
    for l in list:
        if(i<=len(list)-5):
            l.destroy()
            i=i+1
    btn1 = Button(root, text = 'Add a worker', bd = '5', command = clicked_addaworker)
    btn1.grid(row=2,column=1)
    btn2 = Button(root, text = 'View-Edit details of a worker',command=clicked_viewedit_a_worker, bd = '5')
    btn2.grid(row=3,column=1)
    btn3 = Button(root, text = 'Delete details of a worker',command=clicked_delete_a_worker, bd = '5')
    btn3.grid(row=4,column=1)
    
def clicked_addaworker():
        list = root.grid_slaves()
        i=0
        for l in list:
            if(i<=len(list)-5):
                l.destroy()
                i=i+1
        label_ = Label(root, text = "Enter the details of the worker")
        label_.grid(row=2,column=1)
        
        #nameofworker
        l1=Label(root,text='Name of the worker')
        l1.grid(row=3,column=1)
        nameofworker_var=tk.StringVar()
        nameofworker_entry = tk.Entry(root,textvariable=nameofworker_var, font=('calibre',10,'normal'))
        nameofworker_entry.grid(row=3,column=2)
        
        
        #mobile number
        l2=Label(root,text='Mobile Number')
        l2.grid(row=4,column=1)
        mobileno_var=tk.StringVar()
        mobileno_entry = tk.Entry(root,textvariable=mobileno_var ,font=('calibre',10,'normal'))
        mobileno_entry.grid(row=4,column=2)
        
        #Role
        l3=Label(root,text='Role')
        l3.grid(row=5,column=1)
        role_var=tk.StringVar()
        role_entry = tk.Entry(root,textvariable = role_var, font=('calibre',10,'normal'))
        role_entry.grid(row=5,column=2)
        
        #Skill Level
        l4=Label(root,text='Skill Level')
        l4.grid(row=6,column=1)
        skillLevel_var=tk.StringVar()
        skillLevel_entry = tk.Entry(root,textvariable = skillLevel_var, font=('calibre',10,'normal'))
        skillLevel_entry.grid(row=6,column=2)
        
        def submit_addaworker():
            
            Submit_addworker_btn['text']='Saved!'

            mySql_insert_query = """INSERT INTO worker( Name, Mobile_number, Role, Skill_level) VALUES
                           ( %s, %s,%s, %s ) """
            record = (nameofworker_var.get(),mobileno_var.get(),role_var.get(),int(skillLevel_var.get()))
            cursor = connection.cursor()
            cursor.execute(mySql_insert_query,record)
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into Laptop table")
            cursor.close()
        
            def change_phrase_submit():
                Submit_addworker_btn['text']='Submit'
                
            Submit_addworker_btn.after(3000,change_phrase_submit)
            
            
            mysql_update_worker_query="""SELECT Id, No_of_workers_req, Start_date, Requirement, Priority, Status, Duration, workers_allotted, no_of_workers_alloted FROM work WHERE Requirement=%s and Status='Ongoing' and no_of_workers_alloted<No_of_workers_req Order by  Priority;"""
            record=(role_var.get(),)
            cursor = connection.cursor(buffered=True)
            cursor.execute(mysql_update_worker_query,record)
            connection.commit()
            result=cursor.fetchall()
            for row in result:
                clicked_assign_button(int(row[0]),int(row[1]),row[2],row[3],row[8])
            nameofworker_var.set("")
            mobileno_var.set("")
            role_var.set("")
            skillLevel_var.set("")
            cursor.close()
        Submit_addworker_btn=Button(root, text = "Submit",command = submit_addaworker)
        Submit_addworker_btn.grid(row=7,column=1)
        
        

def clicked_viewedit_a_worker():
        list = root.grid_slaves()
        i=0
        for l in list:
            if(i<=len(list)-5):
                l.destroy()
                i=i+1
        label_ = Label(root, text = "View-Edit the details of the worker")
        label_.grid(row=2,column=1)
        Label(root, text = 'Id',bd=10).grid(row=3,column=0)
        Label(root, text = 'Name',bd=10).grid(row=3,column=1)
        Label(root, text = 'Mobile number',bd=10).grid(row=3,column=2)
        Label(root, text = 'Role',bd=10).grid(row=3,column=3)
        Label(root, text = 'Skill level',bd=10).grid(row=3,column=4)
        Label(root, text = 'Availability',bd=10).grid(row=3,column=5)
        Label(root, text = 'hours_worked',bd=10).grid(row=3,column=6)
        Label(root, text = 'works completed',bd=10).grid(row=3,column=7)

        cursor = connection.cursor()
        cursor.callproc('get_worker')
        # print results
        print("Printing laptop details")
        for result in cursor.stored_results():
            print(type(result))
            #print(result.fetchall())
            i=4
            for lists in result.fetchall():

                for j in range(len(lists)):
                    tempLabel=Label(root, text = lists[j],bd=20)
                    tempLabel.grid(row=i,column=j)
                    tempLabel.config( fg= "white")
                Button(root, text = "Edit",command=partial(editaworker,lists[0]),bd=20).grid(row=i,column=8)
                i=i+1


def editaworker(id):
        list = root.grid_slaves()
        i=0
        for l in list:
            if(i<=len(list)-5):
                l.destroy()
                i=i+1      
        
        
        #Id
        l0=Label(root,text='Id')
        l0.grid(row=3,column=1)
        Id_var=tk.StringVar()
        Id_entry = tk.Entry(root,textvariable=Id_var, font=('calibre',10,'normal'))
        Id_entry.grid(row=3,column=2)
        
        
        #nameofworker
        l1=Label(root,text='Name of the worker')
        l1.grid(row=4,column=1)
        nameofworker_var=tk.StringVar()
        nameofworker_entry = tk.Entry(root,textvariable=nameofworker_var, font=('calibre',10,'normal'))
        nameofworker_entry.grid(row=4,column=2)
        
        
        #mobile number
        l2=Label(root,text='Mobile Number')
        l2.grid(row=5,column=1)
        mobileno_var=tk.StringVar()
        mobileno_entry = tk.Entry(root,textvariable=mobileno_var ,font=('calibre',10,'normal'))
        mobileno_entry.grid(row=5,column=2)
        
        #Role
        l3=Label(root,text='Role')
        l3.grid(row=6,column=1)
        role_var=tk.StringVar()
        role_entry = tk.Entry(root,textvariable = role_var, font=('calibre',10,'normal'))
        role_entry.grid(row=6,column=2)
        
        #Skill Level
        l4=Label(root,text='Skill Level')
        l4.grid(row=7,column=1)
        skillLevel_var=tk.StringVar()
        skillLevel_entry = tk.Entry(root,textvariable = skillLevel_var, font=('calibre',10,'normal'))
        skillLevel_entry.grid(row=7,column=2)
        
        #Availability
        l5=Label(root,text='Availability')
        l5.grid(row=8,column=1)
        availability_var=tk.StringVar()
        availability_entry = tk.Entry(root,textvariable = availability_var, font=('calibre',10,'normal'))
        availability_entry.grid(row=8,column=2)
        
        #No_of_hours_worked
        l6=Label(root,text='No of hours worked')
        l6.grid(row=9,column=1)
        No_of_hours_workers_var=tk.StringVar()
        No_of_hours_workers_entry = tk.Entry(root,textvariable = No_of_hours_workers_var, font=('calibre',10,'normal'))
        No_of_hours_workers_entry.grid(row=9,column=2)
        
        #works_completed
        l7=Label(root,text='works_completed')
        l7.grid(row=10,column=1)
        works_completed_var=tk.StringVar()
        works_completed_entry = tk.Entry(root,textvariable = works_completed_var, font=('calibre',10,'normal'))
        works_completed_entry.grid(row=10,column=2)
        
        def submit_addaworker():
            
            Submit_addworker_btn['text']='Saved!'

            cursor = connection.cursor()
            mysql_update_query = """Update worker set  Name=%s, Mobile_number=%s, Role=%s, Skill_level=%s, Availability=%s, No_of_hours_workers=%s, works_completed=%s  where Id =%s """
            record = (nameofworker_var.get(),mobileno_var.get(),role_var.get(),int(skillLevel_var.get()),availability_var.get(),int(No_of_hours_workers_var.get()),works_completed_var.get(),id )
            cursor.execute(mysql_update_query,record)
            connection.commit()
            cursor.close()
            
            nameofworker_var.set("")
            mobileno_var.set("")
            role_var.set("")
            skillLevel_var.set("")
            Id_var.set("")
            availability_var.set("")
            No_of_hours_workers_var.set("")
            works_completed_var.set("")
            
        Submit_addworker_btn=Button(root, text = "Submit",command = submit_addaworker)
        Submit_addworker_btn.grid(row=11,column=1)

        cursor = connection.cursor()
        cursor.callproc('get_worker')
        for result in cursor.stored_results():
            print(type(result))
            for lists in result.fetchall():

                if(lists[0]==id):
                    Id_var.set(lists[0])
                    nameofworker_var.set(lists[1])
                    mobileno_var.set(lists[2])
                    role_var.set(lists[3])
                    skillLevel_var.set(lists[4])
                    availability_var.set(lists[5])
                    No_of_hours_workers_var.set(lists[6])
                    works_completed_var.set(lists[7])
        cursor.close()

def clicked_delete_a_worker():
        list = root.grid_slaves()
        i=0
        for l in list:
            if(i<=len(list)-5):
                l.destroy()
                i=i+1
        label_ = Label(root, text = "Delete the details of the worker")
        label_.grid(row=2,column=1)
        cursor = connection.cursor()
        cursor.callproc('get_worker')
        # print results

        
                    
        def clicked_delete_button(id):
                    print("id in clicked_delete_button is "+str(id))
                    cursor = connection.cursor()
                    cursor.execute("""Delete from worker where Id = %s""",(id,))
                    connection.commit()
                    cursor.close()
        
        
                             
        for result in cursor.stored_results():
            print(type(result))
            #print(result.fetchall())
            i=3
            for lists in result.fetchall():

                for j in range(len(lists)):
                    tempLabel=Label(root, text = lists[j],bd=20)
                    tempLabel.grid(row=i,column=j)
                    tempLabel.config( fg= "white")
                    print("lists[0] in clicked_delete_button is "+str(lists[0]))
                Delete_button=Button(root, text = "Delete",command=partial(clicked_delete_button,lists[0]),bd=20)
                Delete_button.grid(row=i,column=8)
                i=i+1

                

                    
                                    
def assignment_of_workers():
        cursor = connection.cursor()   
        cursor.callproc('works_for_assignment')
        connection.commit()   


        list = root.grid_slaves()
        i=0
        for l in list:
            if(i<=len(list)-5):
                l.destroy()
                i=i+1
        label_ = Label(root, text = "Assigning works to workers")
        label_.grid(row=2,column=1)
        Label(root, text = 'Id',bd=10).grid(row=3,column=0)
        Label(root, text = 'Number of workers req',bd=10).grid(row=3,column=1)
        Label(root, text = 'Start date',bd=10).grid(row=3,column=2)
        Label(root, text = 'Requirement',bd=10).grid(row=3,column=3)
        Label(root, text = 'Priority',bd=10).grid(row=3,column=4)
        Label(root, text = 'Status',bd=10).grid(row=3,column=5)
        Label(root, text = 'Duration',bd=10).grid(row=3,column=6)
        Label(root, text = 'Ids workers',bd=10).grid(row=3,column=7)
        Label(root, text = 'no of workers alloted',bd=10).grid(row=3,column=8)
        # print results

        for result in cursor.stored_results():
            print(type(result))
            #print(result.fetchall())
            i=4
            for lists in result.fetchall():

                for j in range(len(lists)):
                    tempLabel=Label(root, text = lists[j],bd=20)
                    tempLabel.grid(row=i,column=j)
                    tempLabel.config( fg= "white")
                Button(root, text = "Assign",command=partial(clicked_assign_button,lists[0],lists[1],lists[2],lists[3],lists[8]),bd=20).grid(row=i,column=9)
                i=i+1

        cursor.close()
        



            
def clicked_assign_button(id,no_of_workers_required,start_date,requirement,no_of_workers_alloted):
        cursor = connection.cursor()
        args=[requirement,]
        cursor.callproc('get_workers_for_assignment',args)
        connection.commit()   

        top= Toplevel(root)
        top.title('Assigning works to workers')
        top.geometry('500x100')
        list_slaves = top.grid_slaves()
        i=0
        for l in list_slaves:
            if(i<=len(list_slaves)-5):
                l.destroy()
                i=i+1


        workers_alloted_string=''
        stored_Results=cursor.stored_results()
        for result in stored_Results:
            print(type(result))
            #print(result.fetchall())
            i=3
            list_=result.fetchall()
            if(list_==[]):
                Label(top, text = "No workers avaialable").grid(row=3,column=1)
                break
            for lists in list_:
                print(lists)
                print('type of list[5]')
                print(type(lists[5]))
                availability_array_list=list(lists[5])
                print('number of days')
                print((dt.datetime.strptime(start_date, '%d/%m/%Y')-todays_date).days)
                if(availability_array_list[(dt.datetime.strptime(start_date, '%d/%m/%Y')-todays_date).days]=='1' and no_of_workers_alloted < no_of_workers_required):

                    if(workers_alloted_string==''):
                        workers_alloted_string=str(lists[0])
                    else:
                        workers_alloted_string=",".join([workers_alloted_string,str(lists[0])])
                    for i in range((dt.datetime.strptime(start_date, '%d/%m/%Y')-todays_date).days,4):
                        print('i is')
                        print(i)
                        availability_array_list[i]='0'
                    availability_array_string="".join(availability_array_list)
                    cursor_new=connection.cursor()
                    no_of_workers_alloted=no_of_workers_alloted+1
                  
                    mysql_update_work_query = """Update work set workers_allotted=%s,Status=%s, no_of_workers_alloted=%s where Id =%s """
                   
                    mysql_update_worker_query = """Update worker set Availability=%s  where Id =%s """
                    record_work=(workers_alloted_string,'Ongoing',no_of_workers_alloted,id)
                    record_worker=(availability_array_string,lists[0])
                    cursor_new.execute(mysql_update_work_query,record_work)
                    Label(top,text='Workers with following ids are alloted to the chosen work:'+workers_alloted_string).grid(row=1,column=1)
                    print("workin h1re")
                    cursor_new.execute(mysql_update_worker_query,record_worker)
                    print("workin h2re")
                    cursor_new.close()
                    
                    connection.commit()

                    
                    
                    
                    
                    
        cursor.close()
        
if __name__ == '__main__':
    root=tk.Tk()

    #root.geometry("800x533")
    #img=PIL.Image.open("/Users/sukeerthirajeevi/Desktop/python-assignment/imagergb1.png")
    #img_ = ImageTk.PhotoImage(img)  
    #label_bgimg = Label( root, image = img_)
    #label_bgimg.grid(row=0,column=0)
    
    root.title("Project")
    l = Label(root, text = "Work Management System")
    l.config(bg="black",fg="white",font =("Courier", 24))
    l.grid(row=0,column=1)

    global ID_work  
    ID_work=1
    #first 3 buttons
    buttonFont = font.Font(family='Helvetica', size=20, weight='bold')
    btn1 = Button(root, text = 'Works', bd = '10', command = clicked_work,font=buttonFont)
    btn1.grid(row=1,column=0)
    btn1.config(bg='#89CFF0')
    btn2 = Button(root, text = 'Workers', bd = '5', command = clicked_worker,font=buttonFont)
    btn2.grid(row=1,column=1)
    btn3 = Button(root, text = 'Assignment', bd = '10', command = assignment_of_workers,font=buttonFont)
    btn3.grid(row=1,column=2)
    
    print("\n\n")
    print(todays_date)
    
    works_list=work(10,12012022,'plumber',1)
    

    root.mainloop()







