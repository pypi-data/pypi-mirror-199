import math
import matplotlib.pyplot as plt
from TopicFactory import TopicFactory

# Define the input stresses

class mohrsCircle(TopicFactory):
    def __init__(self):
        self.input_dict = {
            "sigmaX": ["", "", "length", "", ""],
            "sigmaY": ["", "", "length", "", ""],
            "tauXY": ["", "", "length", "", ""],
                      }

        self.info = {
             "input": self.input_dict,
             "formula": "",
             "Note": "This is Mohr's Circle",
             "solve_method": "",
             "plot_method": False,
             "Bonus": self.Bonus
             }

    def giveInfo(self):
        return self.info

    def Bonus(self, info):
        return self.selfSolve(info["input"]["sigmaX"][0], info["input"]["sigmaY"][0], info["input"]["tauXY"][0])
    def selfSolve(self, sigma_x, sigma_y, tau_xy):
        Center = (sigma_x + sigma_y)/2
        Radius = math.sqrt(((sigma_x-sigma_y)/2)**2 + tau_xy**2)
        calc1 = Center+Radius
        calc2 = Center-Radius
        case1 = False
        case2 = False

        if (calc1 > 0) & (calc2 <= 0):
            case1 = True
            sigma1 = calc1
            sigma2 = 0
            sigma3 = calc2
        elif (calc1 > 0) & (calc2 > 0):
            case2 = True
            sigma1 = calc1
            sigma2 = calc2
            sigma3 = 0
        else:
            sigma1 = 0
            sigma2 = calc1
            sigma3 = calc2


        tauIn = Radius
        tauAll = abs((sigma1-sigma3)/2)

        if (sigma_x - sigma_y) == 0:
            thetaP = 45
        else:
            thetaP = math.degrees((1/2) * math.atan((2 * tau_xy) / (sigma_x - sigma_y)))

        if tau_xy == 0:
            thetaS = -45
        else:
            thetaS = math.degrees(-(1/2) * math.atan((sigma_x - sigma_y) / (2 * tau_xy)))


        if thetaP > 0:
            thetaP90 = thetaP-90
        else:
            thetaP90 = thetaP+90



        if thetaS > 0:
            thetaS90 = thetaS-90
        else:
            thetaS90 = thetaS+90


        sigmaThetaP = ((sigma_x + sigma_y) / 2) + ((sigma_x - sigma_y) / 2) * math.cos(math.radians(2 * thetaP)) + tau_xy * math.sin(math.degrees(2 * thetaP))
        tauXYThetaS = -((sigma_x - sigma_y) / 2) * math.sin(math.radians(2 * thetaS)) + tau_xy * math.cos(math.degrees(2 * thetaS))
        sigmaThetaP90 = ((sigma_x + sigma_y) / 2) + ((sigma_x - sigma_y) / 2) * math.cos(math.degrees(2 * thetaP90)) + tau_xy * math.sin(math.degrees(2 * thetaP90))


        if sigmaThetaP < sigmaThetaP90:
            thetaP = thetaP90
        if tauXYThetaS < tauIn:
            thetaS = thetaS90


        # Calculate the center and radius of the circles for each plane
        center_xy = [(sigma_x + sigma_y)/2, 0]
        center_xz = [(sigma_x - sigma_y)/2, 0]
        center_yz = [(sigma_y - sigma_x)/2, 0]
        R_xy = math.sqrt((sigma_x - center_xy[0])**2 + tau_xy**2)
        R_xz = math.sqrt(center_xz[0]**2 + tau_xy**2)
        R_yz = math.sqrt(center_yz[0]**2 + tau_xy**2)

        # Define the coordinates of the circles
        theta_c = [i*math.pi/180 for i in range(0, 360)]
        fig, ax1 = plt.subplots()
        ax1.invert_yaxis()


        ax1.axhline(0, color='black', linewidth=1)
        ax1.axvline(0, color='black', linewidth=1)



        if case1:
            xunit = [((sigma1 + abs(sigma3)) / 2) * math.cos(t) + ((sigma1 + sigma3) / 2) for t in theta_c]
            yunit = [((sigma1 + abs(sigma3)) / 2) * math.sin(t) for t in theta_c]
            ax1.plot(xunit, yunit,color='black', linewidth=1.5)

            xunit = [((sigma2+sigma3)/2) * math.cos(t) + ((sigma2+sigma3)/2) for t in theta_c]
            yunit = [((sigma2+sigma3)/2) * math.sin(t)for t in theta_c]
            ax1.plot(xunit, yunit,color='black', linewidth=1.5)

            xunit = [((sigma1+sigma2)/2) * math.cos(t) + ((sigma1+sigma2)/2) for t in theta_c]
            yunit = [((sigma1+sigma2)/2) * math.sin(t) for t in theta_c]
            ax1.plot(xunit, yunit,color='black', linewidth=1.5)
        elif case2:
            xunit = [((sigma1+sigma3)/2) * math.cos(t) + ((sigma1+sigma3)/2) for t in theta_c]
            yunit = [((sigma1+sigma3)/2) * math.sin(t) for t in theta_c]
            ax1.plot(xunit, yunit,color='black', linewidth=1.5)

            xunit = [((sigma2+sigma3)/2) * math.cos(t) + ((sigma2+sigma3)/2) for t in theta_c]
            yunit = [((sigma2+sigma3)/2) * math.sin(t) for t in theta_c]
            ax1.plot(xunit, yunit,color='black', linewidth=1.5)

            xunit = [((sigma1-sigma2)/2) * math.cos(t) + ((sigma1+sigma2)/2) for t in theta_c]
            yunit = [((sigma1-sigma2)/2) * math.sin(t) for t in theta_c]
            ax1.plot(xunit, yunit,color='black', linewidth=1.5)
        else:
            xunit = [((sigma1+sigma3)/2) * math.cos(t) + ((sigma1+sigma3)/2) for t in theta_c]
            yunit = [((sigma1+sigma3)/2) * math.sin(t) for t in theta_c]
            ax1.plot(xunit, yunit,color='black', linewidth=1.5)

            xunit = [((sigma2-sigma3)/2) * math.cos(t) + ((sigma2+sigma3)/2) for t in theta_c]
            yunit = [((sigma2-sigma3)/2) * math.sin(t) for t in theta_c]
            ax1.plot(xunit, yunit,color='black', linewidth=1.5)

            xunit = [((sigma1-sigma2)/2) * math.cos(t) + ((sigma1+sigma2)/2)for t in theta_c]
            yunit = [((sigma1-sigma2)/2) * math.sin(t) for t in theta_c]
            ax1.plot(xunit, yunit,color='black', linewidth=1.5)

        #dots the
        if abs(tauAll-tauIn) > abs(tauIn/100000):
            ax1.scatter(Center,tauIn, color='black', marker='o', s=50)
            ax1.annotate(r"$\tau_{in}$", xy=(Center, (Radius+(Radius/10))))
            ax1.scatter(((sigma1+sigma3)/2),tauAll, color='black', marker='o', s=50)
            ax1.annotate(r"$\tau_{all}$", xy=(((sigma1+sigma3)/2), (tauAll+(Radius/10))))
        else:
            ax1.scatter(Center, tauIn, color='black', marker='o', s=50)
            ax1.annotate(r"$\tau_{in&all}$", xy=(Center, (Radius+(Radius/10))))



        #display dotted angle of theta_p
        upperBound = -2*thetaP
        if upperBound < 0:
            if sigma_x>sigma_y:
                th = [i*math.pi/180 for i in range(0,int(-upperBound))]
                ax1.annotate(r"$\theta_p$", xy=(((Radius/5)+Center),(Radius/10)))
            else:
                th = [i * math.pi / 180 for i in range(-int(180+upperBound),0)]
                ax1.annotate(r"$\theta_p$", xy=(((Radius / 5) + Center), -(Radius / 10)))
        else:
            if sigma_x > sigma_y:
                th = [i * math.pi / 180 for i in range(int(-upperBound),0)]
                ax1.annotate(r"$\theta_p$", xy=(((Radius/5)+Center),(-Radius/10)))
            else:
                th = [i * math.pi / 180 for i in range(0, int(180+upperBound))]
                ax1.annotate(r"$\theta_p$", xy=(((Radius / 5) + Center), (Radius / 10)))
        xunit = [(Radius/5) * math.cos(t) + Center for t in th]
        yunit = [(Radius/5) * math.sin(t) for t in th]
        ax1.plot(xunit, yunit, linestyle='--',color='black', linewidth=1)
        print(upperBound)

        #display dotted angle of theta_s
        if upperBound < 0:
            if sigma_x>sigma_y:
                th = [i*math.pi/180 for i in range( int(-upperBound),90)]
                ax1.annotate(r"$\theta_s$", xy=(Center,tauIn/2.5))
            else:
                th = [i * math.pi / 180 for i in range(90,-int(upperBound-180))]
                ax1.annotate(r"$\theta_s$", xy=(Center, tauIn / 2.5))
        else:
            if sigma_x>sigma_y:
                th = [i * math.pi / 180 for i in range(int((-upperBound)),90)]
                ax1.annotate(r"$\theta_s$", xy=(Center,tauIn/2.5))
            else:
                th = [i * math.pi / 180 for i in range(int(90 + (upperBound)), 270)]
                ax1.annotate(r"$\theta_s$", xy=(Center, -tauIn / 3))

        print(upperBound)
        xunit = [(Radius/3) * math.cos(t) + Center for t in th]
        yunit = [(Radius/3) * math.sin(t) for t in th]
        ax1.plot(xunit, yunit, linestyle='--',color='black', linewidth=1)



        ax1.plot([Center,Center], [0,Radius], linestyle='--', linewidth=1, color="black")
        ax1.scatter(Center,0, color='black', marker='o', s=50)
        ax1.scatter(sigma1,0, color='black', marker='o', s=50)
        ax1.annotate(r"$\sigma_1$", xy=(sigma1,(Radius/10)))
        ax1.scatter(sigma2,0, color='black', marker='o', s=50)
        ax1.annotate(r"$\sigma_2$", xy=(sigma2,(Radius/10)))
        ax1.scatter(sigma3,0, color='black', marker='o', s=50)
        ax1.annotate(r"$\sigma_3$", xy=(sigma3,(Radius/10)))
        ax1.scatter(sigma_x,tau_xy, color='black', marker='o', s=50)
        ax1.annotate(r"$X$", xy=(sigma_x,tau_xy))
        ax1.annotate(r"$Y$", xy=(sigma_y,-tau_xy))
        ax1.scatter(sigma_y,-tau_xy, color='black', marker='o', s=50)
        # Plot the line on all planes where sigma_x = sigma_y
        ax1.plot([sigma_x, sigma_y], [tau_xy, -tau_xy], linestyle='--', color='black',linewidth=1)

        # Set the aspect ratio and axis labels
        ax1.set_aspect('equal', 'box')
        ax1.set_xlabel('Normal stress (MPa)')
        ax1.set_ylabel('Shear stress (MPa)')
        output = {
            "sigma1": [sigma1, "", "length", "", ""],
            "sigma2": [sigma2, "", "length", "", ""],
            "sigma3": [sigma3, "", "length", "", ""],
            "tauIn": [tauIn, "", "length", "", ""],
            "tauAll": [tauAll, "", "length", "", ""],
            "thetaP": [thetaP, "", "length", "", ""],
            "thetaS": [thetaS, "", "length", "", ""],
                      }

        # Add the x and y axes to each plot


        # tau_max_xy = R_xy
        # print(f"Plane XY - Principal stresses: sigma_1 = {sigma_1_xy:.2f} MPa, sigma_2 = {sigma_2_xy:.2f} MPa")
        # print(f"Plane XY - Maximum shear stress: tau_max = {tau_max_xy:.2f} MPa")
        # sigma_1_xz = center_xz[0] + R_xz
        # sigma_2_xz = -sigma_1_xz
        # tau_max_xz = R_xz
        # print(f"Plane XZ - Principal stresses: sigma_1 = {sigma_1_xz:.2f} MPa, sigma_2 = {sigma_2_xz:.2f} MPa")
        # print(f"Plane XZ - Maximum shear stress: tau_max = {tau_max_xz:.2f} MPa")
        # sigma_1_yz = center_yz[0] + R_yz
        # sigma_2_yz = -sigma_1_yz
        # tau_max_yz = R_yz
        # print(f"Plane YZ - Principal stresses: sigma_1 = {sigma_1_yz:.2f} MPa, sigma_2 = {sigma_2_yz:.2f} MPa")
        # print(f"Plane YZ - Maximum shear stress: tau_max = {tau_max_yz:.2f} MPa")
        #
        # # Label the point on the XY plane where the maximum shear stress occurs
        # ax1.annotate(f"({center_xy[0]:.2f}, {tau_max_xy:.2f})", xy=(center_xy[0], tau_max_xy), xytext=(center_xy[0]-1, tau_max_xy+1),
        #             arrowprops=dict(facecolor='black', arrowstyle='->'))


        # Display the plot

        plt.grid(linestyle='--', color='grey', linewidth=0.5)
        plt.show(block='False')
        return output