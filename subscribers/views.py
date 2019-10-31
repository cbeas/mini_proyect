from django.core.paginator import Paginator
from django.views.generic import ListView
from subscribers.models import Subscriber

from django.shortcuts import render
from django.contrib import messages     
import csv, io
from email_validator import validate_email, EmailNotValidError
from datetime import datetime
from django.http import HttpResponse

class SubscriberListView(ListView):
    #show Subscribers, paginate by 10
    model = Subscriber
    template_name = 'subscriber_list.html'  
    context_object_name = 'subscribers'
    paginate_by = 10
    queryset = Subscriber.objects.all()    
    
    

def import_csv(request):
    template="upload_status.html"
    if request.method == 'POST':
        csv_file  = request.FILES['file']
        data_set = csv_file.read().decode('UTF-8')


        if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File must be on CSV format')
                return render(request,template )
         
        io_string = io.StringIO(data_set)        
        i=0
        headersMissing=[]
        emailInvalid=[]
        nameInvalid=[]
        csvList=[]        
        #Validate CSV
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            
            #Check headers
            if i==0:

                if len(column)>=2:
                
                    if column[0].lower()!="fullname":
                        headersMissing.append("fullname")                

                    if column[1].lower()!="email":
                        headersMissing.append("email")
                     
                    if len(headersMissing):
                        messages.error(request, "Headers missing: "+', '.join(headersMissing))
                        return render(request,template )
                else:       
                        messages.error(request, 'CSV file must have 2 headers: fullname, email')
                        return render(request,template )

            #Validate fullname and email
            if i>=1 and len(column)>=2:

                if len(column[0].strip()):
                    fullname=column[0].strip()                    
                else:
                     nameInvalid.append(str(i+1))
                try:
                    # validate and get info
                    v = validate_email(column[1].strip() ) 
                    # replace with normalized form
                    email = v["email"] 
                    csvList.append([fullname,email])
                except EmailNotValidError as e:
                    emailInvalid.append(str(i+1))

           
            i+=1

        if len(emailInvalid):
            messages.error(request, "Invalid email, lines: "+', '.join(emailInvalid))
                
        if len(nameInvalid):
            messages.error(request, "FullName empty, lines: "+', '.join(nameInvalid))

        #Insert and update records
        activeEmails=[]
        if len(emailInvalid)==0 and len(nameInvalid)==0:
            for line in csvList:
                created = Subscriber.objects.update_or_create(full_name=line[0],email=line[1]) 
                activeEmails.append(line[1])

            #Delete Records not imported
            Subscriber.objects.exclude(email__in=activeEmails).delete()
 

    return render(request, "upload_status.html")

def export_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="newsletter_subscribers.csv"'

    writer = csv.writer(response)
    writer.writerow(['fullname', 'email'])   
    for line in Subscriber.objects.all():
        writer.writerow([line.full_name,line.email])
        

    return response