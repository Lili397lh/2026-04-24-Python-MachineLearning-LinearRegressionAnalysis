import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression

def select_csv():
    # Loading CSV
    pth=filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=[("CSV files","*.csv")]
    )
    if not pth:
        return
    global data
    data=pd.read_csv(pth)

    # Delete table from previous data loaded
    table.delete(*table.get_children())

    # ---Side left---
    # Loading of data in table
    columns=list(data.columns)
    table["columns"]=columns
    table["show"]="headings"
    for col in columns:
        table.heading(col,text=col)
        table.column(col,width=100,minwidth=80,stretch=False,anchor="center")
    for _, fila in data.iterrows():
        table.insert("","end",values=list(fila))
    # ---Side right---
    # Load options of comboboxes
    comboboxX["values"]=columns
    comboboxY["values"]=columns
    comboboxFilter["values"]=[""]+columns

def linear_regression():
    # Get values of comboboxes and entry value
    variablex = comboboxX.get()
    variabley = comboboxY.get()
    FilterVariable = comboboxFilter.get()
    FilterSymbol = comboboxSymbol.get()
    value=entryFilter.get()
    
    # Filter
    # Apply filter selected to data of x, y
    if FilterSymbol=="":
        datafiltered=data[[variablex,variabley]]
    else:
        if FilterSymbol=="=":
            datafiltered=data.loc[data[FilterVariable]==value,[variablex,variabley]]
        elif FilterSymbol==">":
            datafiltered=data.loc[data[FilterVariable]>float(value),[variablex,variabley]]
        elif FilterSymbol=="<":
            datafiltered=data.loc[data[FilterVariable]>float(value),[variablex,variabley]]
        elif FilterSymbol==">=":
            datafiltered=data.loc[data[FilterVariable]>=float(value),[variablex,variabley]]
        elif FilterSymbol=="<=":
            datafiltered=data.loc[data[FilterVariable]<=float(value),[variablex,variabley]]

    # Errors in comboboxes and entry value
    errors=[]
    if variablex=="":
        errors.append("- Variable X empty\n")
    if variabley=="":
        errors.append("- Variable Y empty\n")
    if FilterVariable!="" and (value=="" or FilterSymbol==""):
        errors.append("- Selected a filter without a value\n")
    if value!="" and (FilterVariable=="" or FilterSymbol==""):
        errors.append("- Selected a value without a filter or a symbol\n")
    if FilterSymbol!="" and (FilterVariable=="" or value==""):
        errors.append("- Selected a symbol without a filter or a value\n")
    if not data.notnull:
        errors.append("- CSV not selected\n")
    if errors:
        messagebox.showerror("Error","".join(errors))
        return

    # Linear regression of X,Y
    x=datafiltered[[variablex]]
    y=datafiltered[variabley]
    print(x)
    print(y)
    model=LinearRegression()
    model.fit(x,y)
    y_pred=model.predict(x)

    # Representation of data and Linear Regression
    ax.clear()
    ax.scatter(x[variablex],y,color="blue", label="Data")
    ax.plot(x[variablex],y_pred,color="red", label="Linear regression")
    ax.set_xlabel(variablex)
    ax.set_ylabel(variabley)
    ax.legend()
    ax.grid(True)
    canvas.draw()
    
    # Insert Linear Regression results in text box
    Resultstable.delete("1.0","end")
    Resultstable.insert("end",f"Intercept:  {round(model.intercept_,4)}\n")
    Resultstable.insert("end",f"Slope:  {round(model.coef_[0],4)}\n")
    Resultstable.insert("end",f"R^2:  {round(model.score(x,y),4)}\n")

# Terminates when click in close
def close_window():
    plt.close(fig)
    window.destroy()

# Window creation
window=tk.Tk()
window.title("Linear Regression")
window.geometry("1100x600")

# Grid creation of two columns for left and right side
grid=tk.Frame(window)
grid.pack(fill="both", expand=True)
grid.grid_rowconfigure(0,weight=1)
grid.grid_columnconfigure(0,weight=1)
grid.grid_columnconfigure(1,weight=1)

frametable=tk.Frame(grid)
frametable.grid(row=0,column=0,sticky="nsew")
frameright=tk.Frame(grid)
frameright.grid(row=0,column=1,sticky="nsew")
frametable.grid_propagate(False)
frameright.grid_propagate(False)

# ---Side left---
# Grid creation of two rows for button and table
frametable.grid_rowconfigure(0,weight=0) #button
frametable.grid_rowconfigure(1,weight=1) #table
frametable.grid_columnconfigure(0,weight=1)

topframetable=tk.Frame(frametable)
topframetable.grid(row=0,column=0,sticky="ew")
bottomframetable=tk.Frame(frametable)
bottomframetable.grid(row=1,column=0,sticky="nsew")
bottomframetable.grid_rowconfigure(0,weight=1)
bottomframetable.grid_columnconfigure(0,weight=1)

# Button
loadbutton= tk.Button(topframetable,text="Select CSV",command=select_csv)
loadbutton.pack(pady=10)

# Table
# Creation of scroll in X and y and Table
scrolly=ttk.Scrollbar(bottomframetable,orient="vertical")
scrollx=ttk.Scrollbar(bottomframetable,orient="horizontal")
table=ttk.Treeview(bottomframetable,yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
# Grid creation of 2 columns and 2 rows for Table, scroll in X and scroll in Y
table.grid(row=0,column=0,sticky="nsew")
scrolly.grid(row=0,column=1,sticky="ns")
scrollx.grid(row=1,column=0,sticky="ew")
scrolly.config(command=table.yview)
scrollx.config(command=table.xview)

# ---Side right---
# Grid creation of 4 rows for Selectors, filter, plot, and Results
frameright.grid_rowconfigure(0,weight=0) #Selectors
frameright.grid_rowconfigure(1,weight=0) #Filter
frameright.grid_rowconfigure(2,weight=1) #Plot
frameright.grid_rowconfigure(3,weight=0) #Results
frameright.grid_columnconfigure(0,weight=1)
framerightSelectors=tk.Frame(frameright)
framerightSelectors.grid(row=0,column=0,sticky="nw")
framerightFilter=tk.Frame(frameright)
framerightFilter.grid(row=1,column=0,sticky="nw")
framerightPlot=tk.Frame(frameright)
framerightPlot.grid(row=2,column=0,sticky="nsew")
framerightResults=tk.Frame(frameright)
framerightResults.grid(row=3,column=0,sticky="ns")

# Selectors
# Creation of Label and combobox for X
Labelx=ttk.Label(framerightSelectors,text="Select variable X:")
Labelx.pack(side='left', pady=(10,5))
comboboxX = ttk.Combobox(framerightSelectors)
comboboxX.pack(side='left', padx=(10,0), pady=(10,5))
# Creation of Label and combobox for Y
Labely=ttk.Label(framerightSelectors, text="Select variable Y:")
Labely.pack(side='left', padx=(20,0), pady=(10,5))
comboboxY = ttk.Combobox(framerightSelectors)
comboboxY.pack(side='left', padx=(30,0), pady=(10,5))

# Filter
# Creation of label, comboboxes and entry text box
LabelFilter=ttk.Label(framerightFilter,text="Select Filter (Optional):")
LabelFilter.pack(side='left', pady=(10,5))

comboboxFilter = ttk.Combobox(framerightFilter)
comboboxFilter.pack(side='left', padx=(10,0), pady=(10,5))

comboboxSymbol = ttk.Combobox(framerightFilter,values=["","=",">","<",">=","<="],width=4)
comboboxSymbol.pack(side='left', padx=(15,0), pady=(10,5))

entryFilter=tk.Entry(framerightFilter)
entryFilter.pack(side='left', padx=(20,0), pady=(10,5))

# Plot
# Creation of empty plot
fig,ax=plt.subplots()
canvas=FigureCanvasTkAgg(fig,master=framerightPlot)
canvas.draw()
canvas.get_tk_widget().pack(fill="both",expand=True)

# Results
# Creation of empty results
Resultstable=tk.Text(framerightResults,width=20,height=3)
Resultstable.pack(pady=(10,5))
Resultstable.delete("1.0","end")
Resultstable.insert("end",f"Intercept:  -  \n")
Resultstable.insert("end",f"Slope:  -  \n")
Resultstable.insert("end",f"R^2:  -  \n")

Resultsbutton= tk.Button(framerightResults,text="Calculate",command=linear_regression)
Resultsbutton.pack(pady=(10,5))

# closes window when click in X
window.protocol("WM_DELETE_WINDOW",close_window)

window.mainloop()