import cdsapi
import time
years = ['1980','1981','1982','1984','1985','1986','1989','1990','1991','1992','1993','1995','1996','1997','1998','1999','2000','2001','2003','2004','2005','2006','2007','2008','2010','2011','2012','2013']
variables = ['u_component_of_wind','v_component_of_wind','geopotential', 'temperature', 'vertical_velocity','vorticity']
        
def callrequest(i,j,c):
  print("request received for : ",i,j,c)
  duration = 0.001
  present_time = time.time()
  while time.time()<present_time + duration:
         d = c-1
         c = c+1
         if d == 0:
               c = cdsapi.Client()
               c.retrieve(
                   'reanalysis-era5-pressure-levels',
               {
                   'product_type': 'reanalysis',
                   'variable': variables[j],
                   'pressure_level': [
                       '50', '100', '150',
                       '200', '250', '300',
                       '350', '400', '450',
                       '500', '550', '600',
                       '650', '700', '750',
                       '800', '850', '900',
                       '950', '1000',
                  ],
                  'year': years[i],
                  'month': [
                       '01', '02', '03',
                       '04', '05', '06',
                       '07', '08', '09',
                       '10', '11', '12',
                  ],
                  'day': [
                       '01', '02', '03',
                       '04', '05', '06',
                       '07', '08', '09',
                       '10', '11', '12',
                       '13', '14', '15',
                       '16', '17', '18',
                       '19', '20', '21',
                       '22', '23', '24',
                       '25', '26', '27',
                       '28', '29', '30',
                       '31',
                  ],
                  'time': [
                       '00:00', '06:00', '12:00',
                       '18:00',
                  ],
                  'area': [
                       40, 50, -10,
                       120,
                  ],

                  'format': 'netcdf',
               },
               'download.nc')
         else:
            time.sleep(2)

for i in range(len(years)):
    for j in range(len(variables)):
        counter = 1
        callrequest(i,j,counter)
