try:
    from platform import python_version
    import pandas as pd
    from openpyxl import Workbook
    import datetime
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders


    def attendance_report():

        try:
            #opening attendence,students file to data frame
            df1 = pd.read_csv('input_attendance.csv')
            df2 = pd.read_csv('input_registered_students.csv')
            df1 = df1.dropna(axis=0, how='any')#removing empty columns 
            df2 = df2.dropna(axis=0, how='any')#removing empty columns
            df1.reset_index(inplace=True)
            df2.reset_index(inplace=True)
            dates = ['']*len(df1)

            for i in range(0, len(df1)):
                dates[i] = (df1['Timestamp'][i][0:10])

            data = {'r1': dates, 'r2': df1['Attendance']}
            df3 = pd.DataFrame(data)
            df3 = df3.drop_duplicates(
                subset=['r1', 'r2'],
                keep='last').reset_index(drop=True)

            class_dates = set(dates)
            v_dates = []
            n = int(0)
            for i in class_dates:
                da = datetime.datetime.strptime(str(i), '%d-%m-%Y')
                if (da.weekday() == 0 or da.weekday() == 3):
                    n += 1
                    v_dates += [i]

            dict_dup = {}  # creating dictionary to notes number of duplicates by every student at a paricular date
            dict_fake = {}  # crrating dictionary to notes number of fake by every student at a paricular date


            for i in range(len(df3)):
                da = datetime.datetime.strptime(str(df3['r1'][i]), '%d-%m-%Y')
                if df3['r1'][i] not in dict_dup:
                    dict_dup[df3['r1'][i]] = {}
                dict_dup[df3['r1'][i]][df3['r2'][i][0:8]] = int(0)
                if df3['r1'][i] not in dict_fake:
                    dict_fake[df3['r1'][i]] = {}
                dict_fake[df3['r1'][i]][df3['r2'][i][0:8]] = int(0)


            for i in range(0, len(df1)):
                # setting da as object of time as we traverse through attendence
                da = datetime.datetime.strptime(
                    str(df1['Timestamp'][i]), '%d-%m-%Y %H:%M')
                if ((da.weekday() == 0 or da.weekday() == 3) and da.hour == 14):
                    # checks the condition for actual,duplicate,fake attendence
                    dict_dup[df1['Timestamp'][i][0:10]][df1['Attendance'][i][0:8]] += 1
                elif ((da.weekday() == 0 or da.weekday() == 3) and da.hour != 14):
                    dict_fake[df1['Timestamp'][i][0:10]
                            ][df1['Attendance'][i][0:8]] += 1

            sat = [['Roll', 'name']] #consoliadted attendance
            for i in range(1, n+1):
                sat[0] += [f'Date {i}']
            sat[0] += ['Actual Lecture Taken', 'Total Real', '%Attendence']
            sat.insert(1, ['(sorted by roll)', '', 'Atleast one real is P'])
            sat[1] += ['']*n
            sat[1] += ['(=Total Mon+Thru dynamic count)', '',
                        'Real/Actual Lecture Taken (Keep two digits decimal precision e.g., 90.58, round off )']


            for i in range(0, len(df2)):

                colmn = [['Date', 'Roll', 'Name', 'Total Attendence Count',
                    'Real', 'Duplicate', 'Invalid', 'Absent']]
                colmn.insert(len(colmn), ['', df2['Roll No'][i],
                        df2['Name'][i], n, '', '', '', ''])
                sat.insert(len(sat), [df2['Roll No'][i], df2['Name'][i]])
                k = 1
                p = int(0)
                for j in v_dates:
                    if df2['Roll No'][i] not in dict_dup[j]:
                        colmn.insert(len(colmn), [f'Day {k}', '', '', '', 0, 0, 0, 1])

                        sat[len(sat)-1] += 'A'

                    else:
                        r = int(dict_dup[j][df2['Roll No'][i]] > 0)
                        f = 0
                        if (r):
                            f = dict_dup[j][df2['Roll No'][i]]-1
                        inv = dict_fake[j][df2['Roll No'][i]]
                        # creating files for student ,consilidated file
                        a = int(dict_dup[j][df2['Roll No'][i]] == 0)
                        colmn.insert(len(colmn), [f'Day {k}', '', '', '', r, f, inv, a])
                        if (r):
                            sat[len(sat)-1] += 'P'
                            p += 1
                        else:
                            sat[len(sat)-1] += 'A'
                    k += 1
                per = (p/n)*100
                per = "{:.2f}".format(round(per, 2))
                sat[len(sat)-1] += [n, p, per]

                x = './output/'
                x += df2['Roll No'][i]
                x += '.xlsx'
                wb = Workbook()
                sheet = wb.active  # converting the list to xlsx file
                for l in colmn:
                    sheet.append(l)
                wb.save(x)
            
            
            wb = Workbook()

            sheet = wb.active  # converting the list to xlsx file
            for l in sat:
                sheet.append(l)
            wb.save('./output/attendence_report_consolidated.xlsx')

        except FileNotFoundError:
            # if Input file is not found / typo in name of the file
            print("Error : Input File Not Found")
        except PermissionError:
             print("Error: Dont have the permission ,Close the output excel file and code the code again")
        except FileExistsError:
            print("File Already Exists, Deleted the existing output file and run again")


    def send_mail(fromaddr, frompasswd, toaddr, msg_subject, msg_body, file_path):
        try:
            msg = MIMEMultipart()
            print("[+] Message Object Created")  # code for sending mail
        except:
            print("[-] Error in Creating Message Object")
            return

        msg['From'] = fromaddr

        msg['To'] = toaddr

        msg['Subject'] = msg_subject

        body = msg_body

        msg.attach(MIMEText(body, 'plain'))

        filename = file_path
        attachment = open(filename, "rb")

        p = MIMEBase('application', 'octet-stream')

        p.set_payload((attachment).read())

        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        try:
            msg.attach(p)
            print("[+] File Attached")
        except:
            print("[-] Error in Attaching file")
            return

        try:
            s = smtplib.SMTP('stud.iitp.ac.in', 587)
            print("[+] SMTP Session Created")
        except:
            print("[-] Error in creating SMTP session")
            return

        s.starttls()

        try:
            s.login(fromaddr, frompasswd)
            print("[+] Login Successful")
        except:
            print("[-] Login Failed")

        text = msg.as_string()

        try:
            s.sendmail(fromaddr, toaddr, text)
            print("[+] Mail Sent successfully")
        except:
            print('[-] Mail not sent')

        s.quit()


    def isEmail(x):
        if ('@' in x) and ('.' in x):
            return True
        else:
            return False


    def tut_06():
        FROM_ADDR = "goje_2001ee19@iitp.ac.in"
        FROM_PASSWD = "Gsatvik#2410"
        TO_ADDR = "satvikgoje2410@gmail.com"
        Subject = " attendence_report_consolidated of CS384  "
        Body = " Check The attachment "
        file_path = './output/attendence_report_consolidated.xlsx'
        send_mail(FROM_ADDR, FROM_PASSWD, TO_ADDR, Subject, Body, file_path)

except:
    print("Error:Install Required libraries ")
ver = python_version()


attendance_report()
i = input('If You want to check a Consolidated report to mail,Enter Any postive number:')
if (int(i) > 0):
    tut_06()
