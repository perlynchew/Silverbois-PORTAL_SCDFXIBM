# PORTAL

Our rationale - we want to leverage on the capabilities of CFRs to provide timely assistance in the event of accidents, especially for our growing elderly population. As such, we identified the situation where it is the most feasible for CFRs to provide timely assistance - when accidents occur in public spaces. Even though we understand that a proportion of incidents for elderly with no next of kin may happen in their homes, we recognise that there may be contraints for CFRs to provide early intervention as they may not be able to enter the elderly's homes. 

As such, we evaluated the next best situation where we can maximise the potential of CFRs in providing early intervention. Understanding that many elderly with next of kin may go out alone, we felt that there was a shortfall in the detection of such cases. In particular, the current framework still completely relies on the calls by citizens to SCDF, which may not be fast enough in the event that no one notices the casualty. In such cases, the golden period for treatment may be missed. To overcome this shortfall, we felt that the best possible solution would be to leverage on Singapore's wide network of CCTVs, and through making use of AI, sense-make these seemingly random images in order to detect incidents. 

## Machine Learning

We use IBM Watsons Machine Learning to train our A.I to be able to identify incidents. This is done using past data from incidents in Singapore to increase the accuracy in order to prevent false alarms. Our A.I will then be able to distinguish between fires and other EMS and send these information to nearby CFRs so they are able to assist. This allows for detection of such incidents even whey are not seen by any passersby, mobilising the CFRs more efficiently.


## Reinforcement Learning

As PORTAL is rolled out nationwide, we can gather more data and use these to further train our A.I for higher accuracy in detecting such incidents, reducing the number of false alarms.


## Conclusion

Using Machine Learning to auto detect incidents from CCTV images, coupled with the PORTAL (Flask API), we believe that incidents can be detected more quickly without the need for a passerby to notice the casualty. Through the integration of different technologies, the notification will then be immediately sent out to the myResponders app, promoting even earlier intervention by CFRs, which could save many lives. The acceptance of a request by CFRs is also reflected by PORTAL, thus allowing operators to keep track of the presence of people responding to the incident.

