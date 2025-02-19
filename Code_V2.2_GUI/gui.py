from pathlib import Path
from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import tkinter as tk
import requests
import pandas as pd
# import webbrowser
# import time
from tkhtmlview import HTMLLabel
# import mysql.connector
# import pymysql
# import json

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.geometry("1000x600")
window.configure(bg = "#FFFFFF")
window.attributes("-alpha", 1)
window.title("Repo-Schlep")

s_date=StringVar()
u_date=StringVar()
r_name=StringVar()

def submit():
 
    personal_token = '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'
    HEADER = {'Authorization': f'{personal_token}'}
    df = pd.DataFrame()

    since_date=s_date.get()
    until_date=u_date.get()
    repo_name=r_name.get()
    # since_date = input("Enter the initial Date (YYYY-MM-DD):- ")
    # until_date = input("Enter the final Date (YYYY-MM-DD):- ")
    # repo_name =  input("Enter Repo_Name : ") 
    # date_range_parameter = f'{since_date} to {until_date}'
    org_dict = {'Misc': {'total_contributions': 0, 'unique_contributors': 0, "id": []}}
    print(" ")

    n = 1
    total_commits = 0
    while True:
        info_url = f'https://api.github.com/repos/{repo_name}/commits?page={n}&per_page=100&since={since_date}&until={until_date}'
        commit_info = requests.get(info_url, HEADER).json()
        if commit_info:
            no_of_items = len(commit_info)
            #print(no_of_items)
            total_commits = total_commits + no_of_items
            print("Total commits ", total_commits)
            df = pd.concat([df, pd.DataFrame(commit_info)], ignore_index=True)
            n = n + 1
            # print(df.shape)
        else:
            print(" ")
            print("Completed")
            print(" ")
            break

    data = df
    for commit in data['commit']:
        email = commit['author']['email']
        email_end = email.split('@')
        company_name = email_end[1].rsplit('.', 1)  # Split into 2 from right to remove '.com'
        company = company_name[0].capitalize()  # Capitalize the company name

        # If the organization is users.noreply.github.com e.x. mikemorris@users.noreply.github.com, johncowen@users.noreply.github.com, gmail, yahoo id to Misc
        # For Total contributions, increase the count
        # For unique contributors, if email-id is in list, we will skip his commit i.e. multiple commits

        if company == 'Users.noreply.github' or company == 'Gmail' or company == 'Yahoo':
            org_dict['Misc']['total_contributions'] = org_dict['Misc']['total_contributions'] + 1
            if email not in org_dict['Misc']['id']:
                org_dict['Misc']['id'].append(email)  # org id List
                org_dict['Misc']['unique_contributors'] = org_dict['Misc']['unique_contributors'] + 1
        # If organization is not users.noreply.github.com, make a new key as company name.
        else:
            if company in org_dict.keys():
                org_dict[company]['total_contributions'] = org_dict[company]['total_contributions'] + 1
            else:
                org_dict[company] = {'total_contributions': 1, 'unique_contributors': 0, 'id': []}
            if email not in org_dict[company]['id']:
                org_dict[company]['id'].append(email)  # org id List
                org_dict[company]['unique_contributors'] = org_dict[company]['unique_contributors'] + 1
    
    tc=org_dict['Misc']['total_contributions']
    print("Total contributions:")
    print(tc)
    print(" ")
    uc=org_dict['Misc']['unique_contributors']
    print("Unique contributors:")
    print(uc)
    print(" ")
    id=org_dict['Misc']['id']
    print("IDs of Unique contributors:")
    print(id)
    print(" ")

    print("Company Names:")
    company_keys = [get_company for get_company in org_dict.keys()]
    print(company_keys)

    canvas.create_rectangle(
        29.0,
        580.0,
        597.0,
        120.0,
        fill="#FFFFFF", stipple='gray50',
        outline="")

    label1 = tk.StringVar()
    label1 = HTMLLabel(html=f'''<!DOCTYPE html>
                <html lang="en">
                    <head>   
                    </head>
                    <body>
                        
                        <nav class="navbar navbar-default navbar-fixed-top before-color">     
                            <h4><img src="images/1625253269659.png" width="129" height="85">
                            <img src="images/1625253269659.png" width="129" height="85">
                            <img src="images/1625253269659.png" width="129" height="85">
                            <img src="images/1625253269659.png" width="129" height="85"></h4>
                        </nav>

                        <div style="background-color: #ffffff"">               
                            <h2>Your Search Results</h2><br>
                            =======================================                                  
                                <h4>Repository Name</h4><br>
                                    <p>{repo_name}</p><br>
                                    ________________________________________________________________                 
                                <h4>Date Range</h4><br>
                                    <p>{since_date} to {until_date}</p>
                                    ________________________________________________________________   
                                <h4>Total Contributions</h4><br>
                                    <p>{org_dict['Misc']['total_contributions']}</p><br>
                                    ________________________________________________________________   
                                <h4>Unique Contributors</h4><br>
                                    <p>{org_dict['Misc']['unique_contributors']}</p><br> 
                                    ________________________________________________________________           
                                <h4>IDs of Unique Contributors</h4><br>
                                    <p>{org_dict['Misc']['id']}</p><br> 
                                    ________________________________________________________________     
                                <h4>Company Names</h4><br>
                                    <p>{company_keys}</p><br>
                                    ________________________________________________________________     
                                <h4>Output Dictionary including every data</h4>           
                                    <p>{org_dict}</p>
                                    ________________________________________________________________
                                <h4>Open Webpage</h4>
                                    <h5><img src="images/1625253269659.png" width="130" height="85">
                                    <a href="index.html">Repo-Schlep_Result_index.html</a>
                                    <img src="images/1625253269659.png" width="130" height="85"></h5>
                                    =======================================
                        </div>                           
                        
                        <div>
                            <h1>Welcome to Repo Schlep</h1>  
                            <img src="images/1625253269659.png" width="530" height="343">
                            <p>Vivamus congue diam vitae tortor imperdiet congue. Nullam sagittis, tristique diam, ut ullamcorper tellus.</p> 
                            ________________________________________________________________         
                        </div>
                        
                        <div>
                            <h1>Our Team</h1>

                            <h4> <img src="images/team-1.png" width="242" height="242"><span> __</span>
                            <img src="images/team-2.png" width="242" height="242"></h4>
                            <h3>______Akashdeep_________________Apurvaa______</h3>
                                          
                            <h4> <img src="images/team-6.png" width="242" height="242"><span> __</span>
                            <img src="images/team-9.png" width="242" height="242"></h4>
                            <h3>________Rakesh__________________Aakash________</h3>
                                                    
                            <h4> <img src="images/team-3.png" width="242" height="242"><span> __</span>
                            <img src="images/team-5.png" width="242" height="242"></h4>
                            <h3>________Monika_____________________Priti________</h3> 
                            ________________________________________________________________                           
                        </div>

                        <footer>
                            <div>
                                <h4>=============Repo-Schlep=============</h4>
                                <p>Copyright 2021. Repo-Schlep Created By Akashdeep Chand</p>
                                ________________________________________________________________
                            </div>
                        </footer>
                    
                    </body>
                </html>

                ''',)
    label1.pack(pady=(140,40),
        padx=(50,425),
        fill='both',
        expand=True)    

    s_date.set("")
    u_date.set("")
    r_name.set("") 

    html_content = f'''\<!DOCTYPE html>
    <!--
        Bonativo by TEMPLATE STOCK
        templatestock.co @templatestock
        Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
    -->

    <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Repo-Schlep</title>

            <!-- Bootstrap -->
            <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet">
            <link href="css/style.css" rel="stylesheet" type="text/css">
            <link href="css/flexslider.css" rel="stylesheet" type="text/css">
            <link href="icons/css/ionicons.min.css" rel="stylesheet" type="text/css">
            <link href="icons/css/simple-line-icons.css" rel="stylesheet" type="text/css">
        
            <!--revolution slider setting css-->
            <link href="rs-plugin/css/settings.css" rel="stylesheet">
            <link href="css/prettyPhoto.css" rel="stylesheet" type="text/css" />
            <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
            <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
            <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
            <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
            <![endif]-->
        </head>
        <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.6.9/angular.min.js"></script>
        <body data-spy="scroll" data-target=".navbar" data-offset="80">

            <!-- Static navbar -->
            <nav class="navbar navbar-default navbar-fixed-top before-color">
                <div class="container">
                    <div class="navbar-header">
                        <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-controls="navbar">
                            <span class="sr-only">Toggle navigation</span>
                            <span class="icon-bar"></span>
                            <span class="icon-bar"></span>
                            <span class="icon-bar"></span>
                        </button>
                        <img src="images/1625253269659.png" width="82" height="55">
                        <a class="navbar-brand alo" href="index.html">Repo-Schlep</a>
                    </div>
                    <div id="navbar" class="navbar-collapse collapse">
                        <ul class="nav navbar-nav navbar-right scroll-to">
                            <li class="active"><a href="#home">Home</a></li>
                            <li><a href="#services">Search by repository</a></li>
                            <li><a href="#work">Search by date</a></li>
                            <li><a href="#blog">Our Experience</a></li>
                            <li><a href="#contact">Contact us</a></li>

                        </ul>
                    </div><!--/.nav-collapse -->
                </div><!--/.container-fluid -->
            </nav>

            <section id="home" class="section-padding2">
                <div class="container">
                    <div class="row">

                            <div class="col-sm-10 col-sm-offset-1 text-center" style="background-color: rgba(0, 0, 0, 0.164);">
                                <div class="section-title" style="background-color: rgba(255, 255, 255, 0.6);">
                                    <h1>Your <span class="colored-text">Search Results</span></h1> 
                                    <span class="border-line"></span>
                                    
                                </div>
                                <table class="table text-left" style="background-color: rgba(255, 255, 255, 0.6);">
                                    <thead class="table-primary">
                                    <tr class="table-primary">
                                        
                                        <th scope="col">Repository Name</th>
                                        <th scope="col">Initial Date</th>
                                        <th scope="col">Final Date</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr class="">
                                        
                                        <td>{repo_name}</td>
                                        <td>{since_date}</td>
                                        <td>{until_date}</td>
                                    </tr>
                                    
                                    </tbody>
                                </table>
                                <table class="table text-left" style="background-color: rgba(255, 255, 255, 0.6);">
                                    <thead class="table-primary">
                                    <tr class="table-primary">
                                        
                                        <th scope="col">Total Contributions</th>
                                        <th scope="col" style="background-color: rgba(228, 250, 255, 0.349);">Unique Contributors</th>
                                        <th scope="col" style="background-color: rgba(228, 250, 255, 0.6);">IDs of Unique Contributors</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr class="">
                                        
                                        <td>{org_dict['Misc']['total_contributions']}</td>

                                        <td style="background-color: rgba(228, 250, 255, 0.349);">{org_dict['Misc']['unique_contributors']}</td>

                                        <td style="background-color: rgba(228, 250, 255, 0.6);">
                                            <div data-ng-app="" data-ng-init="ids={org_dict['Misc']['id']}; company={company_keys}">
                                                <ul>
                                                    <li data-ng-repeat="x in ids">
                                                        {{{{ x }}}}
                                                    </li>
                                                </ul><br>
                                                <h4><span>Company Names</span> </h4><hr>
                                                <ul>
                                                    <li data-ng-repeat="y in company">
                                                        {{{{ y }}}}
                                                    </li>
                                                </ul>
                                            </div>
                                        </td>
                                    </tr>
                                    
                                    </tbody>
                                </table>
                                
                                <table class="table text-left" style="background-color: rgba(255, 255, 255, 0.6);">
                                    <thead class="thead-light">
                                    <tr>
                                        <th scope="col">Output Dictionary including every data</th>
                                        
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr>
                                        <td style="font-style: italic; background-color: rgba(228, 250, 255, 0.6);">
                                            {org_dict}
                                        </td>
                                    </tr>
                                    
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div><!--heading row-->
                </div>
            </section><!--work section end-->
            <!-- <section id="blog" > -->
            
                <div  class="testimonials parallax-2">
                    <div class="container">
                        <div class="row">
                            <div class="col-sm-8 col-sm-offset-2 text-center">
                                <div class="section-title text-center">
                                    <h1><span class="colored-text2">Welcome to </span><span class="colored-text1">Repo Schlep</span></h1>  
                                    <span class="border-line1"></span>
                                    
                                </div>
                                <div class="flexslider testislider">
                                    <ul class="slides">
                                        <li>
                                            <div class="slide-items">
                                                <!-- <img src="images/team-1.jpg" alt=""> -->
                                                <p>
                                                    <span class="colored-text1">Vivamus congue diam vitae tortor imperdiet congue. Nullam sagittis, tristique diam, ut ullamcorper tellus.</span> 
                                                </p>
                                                <h2><span class="colored-text2">Maria Navratilova</span></h2>
                                            </div>
                                        </li>
                                        <li>
                                            <div class="slide-items">
                                                <!-- <img src="images/team-2.jpg" alt=""> -->
                                                <p>
                                                    <span class="colored-text1">Vivamus congue diam vitae tortor imperdiet congue. Nullam sagittis, tristique diam, ut ullamcorper tellus.</span> 
                                                </p>
                                                <h2><span class="colored-text2">Maria Navratilova</span></h2>
                                            </div>
                                        </li>
                                        
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div><!--testimonials-->
            <!-- </section> -->

            <section id="services" class="section-padding1">
                <div class="container">
                    <div class="row">
                        <div class="col-sm-8 col-sm-offset-2 text-center">
                            <div class="section-title">
                                <h1>Search by <span class="colored-text">Repository</span></h1> 
                                <span class="border-line"></span>
                                
                            </div>
   
                            <!-- <div class="col-sm-6 col-sm-offset-3"> -->
                                <form name="" class="contact-form1" method="post" >
                                
                                    <div class="row">
                                        <div class="col-md-12" >
                                            <div class="row control-group">
                                                <div class="form-group col-xs-12 controls">
                                                    
                                                    <input type="text" class="form-control1" placeholder="Repository Name" id="name" required data-validation-required-message="Please enter Repository name.">
                                                    <p class="help-block"></p>
                                                    
                                                </div>
                                            </div>
                                        </div>
                                        <div class="form-group col-xs-12 text-right">
                                            <button type="submit" class="btn btn-outline-dark btn-lg">Search</button>
                                        </div>
                                    </div>
                                
                                </form>    
                        <!-- </div>         -->
                        </div>
                    </div><!-- title row end-->
                </div>
            </section>

            <section id="work" class="section-padding1">
                <div class="container">
                    <div class="row" style="background-color: rgba(0, 0, 0, 0.164);">
                        
                            <div class="col-sm-8 col-sm-offset-2">
                                <div class="section-title text-center" style="background-color: rgba(255, 255, 255, 0.6);">
                                    <h1>Search by <span class="colored-text">Date</span></h1>  
                                    <span class="border-line"></span>
                                    
                                </div>
                                
                                <form name="" class="contact-form1" method="post" style="background-color: rgba(255, 255, 255, 0.6);">
                                <div class="row">
                                    <div class="col-md-12" >
                                        <div class="row control-group">
                                            <div class="form-group col-xs-12 controls">
                                                
                                                <input type="text" class="form-control2" placeholder="Repository Name" id="name" required data-validation-required-message="Please enter Repository name.">
                                                <p class="help-block"></p>
                                                
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-sm-6">
                                        <div class="row control-group">
                                            <div class="form-group col-xs-12 controls">
                                        
                                                <input type="date" class="form-control3" id="name" placeholder="Date From" value="" required>
                                        
                                            </div>
                                        </div>
                                    </div>
                        
                                    <div class="col-sm-6">
                                    
                                        <input type="date" class="form-control3" id="name" placeholder="Date Until" value="" required>
                                        
                                    </div>
                                    <div class="form-group col-xs-12 text-right">
                                        <button type="submit" class="btn btn-outline-dark btn-lg">Search</button>
                                    </div>
                                
                                </div>
                                </form>
                            </div>
                        </div>
                    </div><!--heading row-->
                </div>
            </section><!--work section end-->

            <section id="blog" >
            
            <div  class="testimonials parallax-2">
                <div class="container">
                    <div class="row">
                        <div class="col-sm-8 col-sm-offset-2 text-center">
                            <div class="section-title text-center">
                                <h1><span class="colored-text3">Our </span><span class="colored-text4">Experience</span></h1>  
                                <span class="border-line1"></span>
                                
                            </div>
                            <div class="flexslider testislider">
                                <ul class="slides">
                                    <li>
                                        <div class="slide-items">
                                            <img src="images/team-1.png" alt="">
                                            <p>
                                                Vivamus congue diam vitae tortor imperdiet congue. Nullam sagittis, tristique diam, ut ullamcorper tellus. 
                                            </p>
                                            <h2><span class="colored-text3">Akashdeep</span></h2>
                                        </div>
                                    </li>
                                    <li>
                                        <div class="slide-items">
                                            <img src="images/team-2.png" alt="">
                                            <p>
                                                Vivamus congue diam vitae tortor imperdiet congue. Nullam sagittis, tristique diam, ut ullamcorper tellus. 
                                            </p>
                                            <h2><span class="colored-text3">Apurvaa</span></h2>
                                        </div>
                                    </li>
                                    <li>
                                        <div class="slide-items">
                                            <img src="images/team-3.png" alt="">
                                            <p>
                                                Vivamus congue diam vitae tortor imperdiet congue. Nullam sagittis, tristique diam, ut ullamcorper tellus.
                                            </p>
                                            <h2><span class="colored-text3">Monika</span></h2>
                                        </div>
                                    </li>
                                    <li>
                                        <div class="slide-items">
                                            <img src="images/team-4.png" alt="">
                                            <p>
                                                Vivamus congue diam vitae tortor imperdiet congue. Nullam sagittis, tristique diam, ut ullamcorper tellus. 
                                            </p>
                                            <h2><span class="colored-text3">Yash</span></h2>
                                        </div>
                                    </li>
                                    <li>
                                        <div class="slide-items">
                                            <img src="images/team-5.png" alt="">
                                            <p>
                                                Vivamus congue diam vitae tortor imperdiet congue. Nullam sagittis, tristique diam, ut ullamcorper tellus. 
                                            </p>
                                            <h2><span class="colored-text3">Priti</span></h2>
                                        </div>
                                    </li>
                                    <li>
                                        <div class="slide-items">
                                            <img src="images/team-6.png" alt="">
                                            <p>
                                                Vivamus congue diam vitae tortor imperdiet congue. Nullam sagittis, tristique diam, ut ullamcorper tellus.
                                            </p>
                                            <h2><span class="colored-text3">Rakesh</span></h2>
                                        </div>
                                    </li>
                                    <li>
                                        <div class="slide-items">
                                            <img src="images/team-7.png" alt="">
                                            <p>
                                                Vivamus congue diam vitae tortor imperdiet congue. Nullam sagittis, tristique diam, ut ullamcorper tellus. 
                                            </p>
                                            <h2><span class="colored-text3">Vedansh</span></h2>
                                        </div>
                                    </li>
                                    <li>
                                        <div class="slide-items">
                                            <img src="images/team-8.png" alt="">
                                            <p>
                                                Vivamus congue diam vitae tortor imperdiet congue. Nullam sagittis, tristique diam, ut ullamcorper tellus. 
                                            </p>
                                            <h2><span class="colored-text3">Vitthal</span></h2>
                                        </div>
                                    </li>
                                    <li>
                                        <div class="slide-items">
                                            <img src="images/team-9.png" alt="">
                                            <p>
                                                Vivamus congue diam vitae tortor imperdiet congue. Nullam sagittis, tristique diam, ut ullamcorper tellus.
                                            </p>
                                            <h2><span class="colored-text3">Aakash</span></h2>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div><!--testimonials-->
            </section>
            <section id="contact" class="section-padding">
                <div class="container">
                    <div class="row">
                        <div class="col-sm-6 col-sm-offset-3">

                            <form name="sentMessage" class="contact-form" method="post" novalidate>
                                <h3>Drop us a line</h3>
                                <div class="row">
                                    <div class="col-md-12">
                                        <div class="row control-group">
                                            <div class="form-group col-xs-12 controls">

                                                <input type="text" class="form-control" placeholder="Name" id="name" required data-validation-required-message="Please enter your name.">
                                                <p class="help-block"></p>
                                            </div>
                                        </div>

                                    </div>

                                    <div class="col-md-12">
                                        <div class="row control-group">
                                            <div class="form-group col-xs-12 controls">

                                                <input type="email" class="form-control" placeholder="Email Address" id="email" required data-validation-required-message="Please enter your email address.">
                                                <p class="help-block"></p>
                                            </div>
                                        </div> 
                                    </div>
                                </div>
                                <div class="row control-group">
                                    <div class="form-group col-xs-12  controls">

                                        <input type="tel" class="form-control" placeholder="Phone Number" id="phone" required data-validation-required-message="Please enter your phone number.">
                                        <p class="help-block"></p>
                                    </div>
                                </div>
                                <div class="row control-group">
                                    <div class="form-group col-xs-12 controls">

                                        <textarea rows="5" class="form-control" placeholder="Message" id="message" required data-validation-required-message="Please enter a message."></textarea>
                                        <p class="help-block"></p>
                                    </div>
                                </div>
                                <br>
                                <div id="success"></div>
                                <div class="row">
                                    <div class="form-group col-xs-12 text-right">
                                        <button type="submit" class="btn btn-white btn-lg">Send Message</button>
                                    </div>
                                </div>
                            </form>

                        </div>
                    </div>
                </div>
            </section><!--contact section end-->

            <footer class="footer">
                <div class="container text-center">
                    <span class="alo">Repo-Schlep</span>
                    
                    <span class="copyright">&copy; Copyright 2021. Repo-Schlep Created By Conquistadors</span>
                </div>
            </footer>
            <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
            <script src="js/jquery.min.js" type="text/javascript"></script>
            <script src="js/moderniz.min.js" type="text/javascript"></script>
            <script src="js/jquery.easing.1.3.js" type="text/javascript"></script>
            <!-- bootstrap js-->
            <script src="bootstrap/js/bootstrap.min.js" type="text/javascript"></script>
            <script type="text/javascript" src="js/jquery.flexslider-min.js"></script>
            <script type="text/javascript" src="js/parallax.min.js"></script> 
            <script type="text/javascript" src="js/jquery.prettyPhoto.js"></script>	       
            <script type="text/javascript" src="js/jqBootstrapValidation.js"></script>
            <!--revolution slider scripts-->
            <script src="rs-plugin/js/jquery.themepunch.tools.min.js" type="text/javascript"></script>
            <script src="rs-plugin/js/jquery.themepunch.revolution.min.js" type="text/javascript"></script>  
            <script src="js/template.js" type="text/javascript"></script>

        </body>
    </html>
    '''
    with open('index.html', "w") as html_file:
        html_file.write(html_content)
        print("Successful")

    ###########  Database
    # connection = pymysql.connect(host="localhost", user="root", passwd="", database="repo-schle")
    
    # table='create table if not exists Data_1(Username_Repository text,Since_Date text,Until_Date text, Total_Contributions text, Unique_Contributors text, IDs_of_Unique_Contributors text, Company_Names text)'
    # insert='insert into data_1 (repo_name, since_date, until_date, tc, uc) values(%s,%s,%s,%s,%s)'
    # values=(repo_name, since_date, until_date, tc, uc)
    # cur=connection.cursor()
    # cur.execute(table)
    # cur.execute(insert,values)
    # connection.commit()
    
    # sql = "INSERT INTO ep_soft(ip_address, id, company_names) VALUES (%s, %s, %s)"
    # cur.execute(sql, ("localhost", json.dumps(id,company_keys)))

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas_bg = PhotoImage(
    file=relative_to_assets("Size.png"))

canvas.create_image(
    550,
    300,
    image=canvas_bg)

canvas.create_rectangle(
    630.0,
    20.0,
    980.0,
    580.0,
    fill="#FFFFFF", stipple='gray50',
    outline="")

canvas.create_rectangle(
    650.0,
    120.0,
    960.0,
    560.0,
    fill="#FFFFFF",
    outline="")

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    805.0,
    201.0,
    image=entry_image_1
)
entry_1 = Entry(textvariable= r_name,
    bd=0,
    bg="#FFFAFA",
    highlightthickness=0,
    font=("Roboto Light Italic", 14 * -1, "italic")
)
entry_1.place(
    x=690.0,
    y=190.0,
    width=230.0,
    height=30.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    805.0,
    300.0,
    image=entry_image_2
)
entry_2 = Entry(textvariable= s_date,
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0,
    font=("Roboto Light Italic", 14 * -1, "italic")
)
entry_2.place(
    x=690.0,
    y=289.0,
    width=230.0,
    height=30.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    805.0,
    399.0,
    image=entry_image_3
)
entry_3 = Entry(textvariable= u_date,
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0,
    font=("Roboto Light Italic", 14 * -1, "italic")
)
entry_3.place(
    x=690.0,
    y=388.0,
    width=230.0,
    height=30.0
)

canvas.create_text(
    691.0,
    372.0,
    anchor="nw",
    text="yyyy-mm-dd",
    fill="#656565",
    font=("Roboto Light Italic", 12 * -1)
)

canvas.create_text(
    692.0,
    273.0,
    anchor="nw",
    text="yyyy-mm-dd",
    fill="#656565",
    font=("Roboto Light", 12 * -1)
)

canvas.create_text(
    691.0,
    175.0,
    anchor="nw",
    text="username/repository",
    fill="#656565",
    font=("Roboto Light", 12 * -1)
)

canvas.create_text(
    691.0,
    351.0,
    anchor="nw",
    text="Until Date",
    fill="#000000",
    font=("Roboto Light", 15 * -1)
)

canvas.create_text(
    692.0,
    251.0,
    anchor="nw",
    text="Since Date",
    fill="#000000",
    font=("Roboto Light", 15 * -1)
)

canvas.create_text(
    691.0,
    151.0,
    anchor="nw",
    text="Enter Repository",
    fill="#000000",
    font=("Roboto Light", 15 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    #command=lambda: print("button_1 clicked"),
    command=submit,
    relief="flat"
)
button_1.place(
    x=772.0,
    y=472.0,
    width=67.0,
    height=67.0
)

canvas.create_text(
    719.0,
    67.0,
    anchor="nw",
    text="Enter the details",
    fill="#000000",
    font=("rage italic", 32 * -1)
)

canvas.create_rectangle(
    29.0,
    20.0,
    597.0,
    106.0,
    fill="#FFFFFF", stipple='gray25',
    outline="")

canvas.create_text(
    200.0,
    35.0,
    anchor="nw",
    text="Repo-Schlep",
    fill="#FFFFFF",
    font=("rage italic", 48 * -1),
)

window.resizable(False, False)
window.mainloop()
