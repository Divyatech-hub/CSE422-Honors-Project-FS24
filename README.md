# CSE422-Honors-Project-FS24
# Topic - NIC Gateway Optimization

### By - Divyalakshmi

## Introduction
This is my submisison for the honors project in CSE 422 - Computer Networks at Michigan State University. This proejct aims to optimize network performance by dynamically selecting the best Network Interface Card (NIC) based on real-time latency measurements. The system continuously monitors multiple NICs, pings selected target websites, and determines the optimal NIC for network traffic based on the lowest Round-Trip Time (RTT). The implementation includes a real- time dashboard using Streamlit to visualize NIC performance.

## Tech Stack
![Matplotlib](https://github.com/user-attachments/assets/5ba8119f-34a5-4f06-b4da-a2312e68310b)
![Pandas](https://github.com/user-attachments/assets/f39a5bb8-5934-409e-a4a3-3acb02b68fbb)
![Streamlit](https://github.com/user-attachments/assets/4b45c326-0882-400e-a210-7fa2631baa3c)
![Netifaces](https://github.com/user-attachments/assets/3621253f-79b4-4ff1-a733-aca57e278093)
![Python](https://github.com/user-attachments/assets/1b364753-bf0e-4c37-99f6-cf23787d57be)


## Setup and Execution Steps

1. In a terminal session, SSH into the remote server.
   
   ``ssh firstname@IP_ADDRESS``
   ``password: PID``
2. Clone this github repository.
3. Change the directory to where the Python file resides.
4. Ensure dependencies are installed.
   
   `` sudo pip3 install streamlit pandas netifaces matplotlib``
5. Run the Python program to launch the Steamlit app. This takes a while to complete its execution, i.e. pinging all the respective target websites to get the data for the RTTs.
   
  `` streamlit run honorsfinal1.py ``
  
6. Open another terminal session side by side. Implement Port Forwarding using the following command:
   
  `` ssh -L [PORT # used by Streamlit]:[IP Address of Remote Server]:[PORT # used by Streamlit]: -N -f [netid]@scully.egr.msu.edu ``

  `` Example: ssh -L 8501:35.9.42.236:8501 -N -f varadhad@scully.egr.msu.edu ``
  
7. Access the NIC GUI Dashboard by navigating to

   ``http://localhost:[PORT # used by Streamlit]``
   
   `` Example: http://localhost:8501``

## GUI Screenshots

<img width="829" alt="Dashboard" src="https://github.com/user-attachments/assets/d6f5cd16-24db-444a-a878-6b3e80d8e020" />
<img width="1507" alt="Screenshot 2025-02-11 at 12 09 07 AM" src="https://github.com/user-attachments/assets/6e80fb04-c68d-4c3c-8128-8b4ca621c5a2" />

## Future Plans
1. Extend Performance Metrics: Include packet loss, jitter, and bandwidth alongside RTT measurements.
2. Enhance Visualization: Add real-time alerts and a comparison mode for historical NIC performance.
3. Mobile-Friendly UI: Optimize the Streamlit dashboard for viewing on mobile devices.
4. Predicting RTT with AI: Using linear regression (or other models) to predict RTT based on history for a particular destination IP address.


## References
1. Python Netifaces Documentation: https://pypi.org/project/netifaces/
2. Streamlit Documentation: https://docs.streamlit.io/
3. Linux Networking Commands: https://linux.die.net/man/









