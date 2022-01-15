from django.shortcuts import render
import math

# Create your views here.

def calc(request):
    if request.method == 'POST':

        n = int(request.POST["n"]) #number of recesses
        L = float(request.POST["L"]) #Axial length
        D = float(request.POST["D"]) #Journal Diameter
        a = float(request.POST["a"]) #Axial side landwidth
        b = float(request.POST["b"]) #Inter-recess land width
        Ps = float(request.POST["Ps"]) #Supply pressure
        Pr = float(request.POST["Pr"]) #Recess pressure
        h0 = float(request.POST["h0"]) #film thickness
        visc = float(request.POST["visc"]) #viscosity
        N = float(request.POST["N"]) #bearing angular speed
        theta = float(request.POST["theta"]) #inter recess angle*(bridge angle)
        x = request.POST["x"] #restrictor type
        
        #-------------------------Flow Rate---------------------------
        beta = Pr/Ps #pressure ratio
        ff = (math.pi*D)/(6*a) #flow factor, also known as beta-dash
        #q0 = flow rate
        q0 = (Ps*(h0**3)/visc)*beta*ff

        #--------------------------Stiffness-----------------------
        gam = (n*a*(L-a))/(math.pi*D*b)

        print(gam)
        if x == "capillary":
            z = beta/(1-beta)
        elif x == "orifice":
            z = 0.5*beta/(1-beta)
        elif x == "constant flow":
            z = 0
        print(z)
        #lambda = stiffness
        lamb = (Ps*L*D*3*(n**2)*beta*(1-(a/L))*((math.sin(math.pi/n))**2))/(h0*2*math.pi*(z+1+(2*gam*((math.sin(math.pi/n))**2))))


        #-----------------------Pumping Power----------------------

        Hp = Ps*q0

        #----------------------Friction Power----------------------

        A = math.pi*D*L
        Ar = math.pi*D*L*(1-(2*a/L))*(1-(n*theta/360))

        Af = A - 0.75*Ar #Friction Area

        U = math.pi*D*N #sliding speed
        #Friction power
        Hf = (visc*Af*(U**2))/h0


        #---------------------------Results------------------------
        Flow_Rate = round(q0,3)
        Stiffness = round(lamb,3)
        Pumping_power = round(Hp,3)
        Friction_power =round(Hf,3)
        Friction_power = str(Friction_power)

        return render(request,'results.html',{'Flow_Rate':Flow_Rate, 'Stiffness':Stiffness, 'Pumping_power':Pumping_power,'Friction_power':Friction_power,'n':n, 'L':L, 'D':D, 'a':a, 'b':b, 'Ps':Ps, 'Pr':Pr, 'h0':h0, "visc":visc, "N":N, "theta":theta})    
    return render(request, 'calci.html')