import netifaces
import subprocess
import os
import time
import datetime
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


class Interface:
    def __init__(self):
        """Initialize the NIC selection and performance tracking"""
        self.nics = [iface for iface in netifaces.interfaces() if iface != "lo"]
        self.nic_ips = self.get_nic_ips()  # Get IPs of NICs
        self.targets = ["google.com", "youtube.com", "stackoverflow.com", "gmail.com", "msu.edu"]

        self.time_wait = 1  # Wait time in seconds
        self.iterations = 5  # Number of RTT tests per NIC

        self.control_data = {"timestamp": [], "nic": [], "website": [], "average": []}
        self.performance_log = {"before": [], "after": []}
        self.cur_nic = None

        print("Interface initialized:", self.nic_ips)

        # Enable IP forwarding for Internet sharing
        self.enable_ip_forwarding()

    def enable_ip_forwarding(self):
        """Enable IP forwarding to act as a gateway"""
        os.system("sudo sysctl -w net.ipv4.ip_forward=1")
        os.system("sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")

    def get_nic_ips(self):
        """Retrieve IP addresses assigned to available NICs"""
        nic_ips = {}
        for iface in self.nics:
            addrs = netifaces.ifaddresses(iface).get(netifaces.AF_INET)
            if addrs:
                nic_ips[iface] = addrs[0]['addr']
        return nic_ips

    def start(self):
        """Runs NIC selection and optimization tests"""
        for iteration in range(self.iterations):
            print("Press Ctrl-C to cancel")
            self.select_nic()
            print(f"Completed Iteration {iteration}")
            print(f"Waiting {self.time_wait} seconds...")
            time.sleep(self.time_wait)

    def ping_targets(self, nic):
        """Pings a set of targets and handles errors gracefully."""
        ret = []
        nic_ip = self.nic_ips.get(nic, None)

        if not nic_ip:
            print(f"Skipping {nic}, no assigned IP.")
            return ret

        print(f"Pinging via {nic} (IP: {nic_ip})")

        for target in self.targets:
            try:
                result = subprocess.run(
                    f"ping -I {nic_ip} -c 1 {target}",
                    shell=True,
                    capture_output=True,
                    text=True
                )
                output = result.stdout.strip()

                # Extract RTT value from output
                rtt_values = []
                for line in output.split("\n"):
                    if "time=" in line:
                        try:
                            rtt_value = float(line.split("time=")[1].split(" ")[0])
                            rtt_values.append(rtt_value)
                        except (ValueError, IndexError):
                            print(f"⚠️ Could not extract RTT from line: {line}")

                if rtt_values:
                    avg_rtt = round(sum(rtt_values) / len(rtt_values), 2)
                    print(f"  - RTT: {avg_rtt} ms")
                    ret.append({"nic": nic, "website": target, "rtt": avg_rtt})
                else:
                    print(f"❌ No RTT data for {target}, skipping.")

            except Exception as e:
                print(f"Error while pinging {target} via {nic_ip}: {e}")

        return ret

    def test_nic(self, nic=None, stage="before"):
        """Runs RTT tests before and after optimization"""
        if not self.cur_nic:
            print(f"⚠️ No NIC selected! Running NIC selection first.")
            self.select_nic()

        print(f"Testing NIC at stage: {stage}")
        for _ in range(self.iterations):
            timestamp = datetime.datetime.now()
            times = self.ping_targets(nic or self.cur_nic)

            if times:
                avg_rtt = sum(entry["rtt"] for entry in times) / len(times)
                websites = ", ".join(entry["website"] for entry in times)
            else:
                avg_rtt = float('inf')
                websites = "N/A"

            # Append data correctly
            self.control_data["timestamp"].append(timestamp)
            self.control_data["nic"].append(nic or self.cur_nic)
            self.control_data["website"].append(websites)
            self.control_data["average"].append(avg_rtt)

            self.performance_log[stage].append(avg_rtt)
            print(f"Logged {avg_rtt} ms for {stage}")

    def select_nic(self):
        """Selects the best NIC dynamically"""
        print("Testing NICs for best latency...")

        avgs = []
        for nic in self.nics:
            print(f"Testing NIC: {nic}")
            times = self.ping_targets(nic)

            avg = sum(entry["rtt"] for entry in times) / len(times) if times else float('inf')
            avgs.append(avg)

        self.cur_nic = self.nics[avgs.index(min(avgs))]
        print(f"✅ Selected NIC: {self.cur_nic}")


# Initialize NIC selection and performance tests
if __name__ == '__main__':
    interface = Interface()

    interface.test_nic(stage="before")
    interface.start()
    interface.test_nic(stage="after")

    before_avg = (
        sum(interface.performance_log["before"]) / len(interface.performance_log["before"])
        if interface.performance_log["before"]
        else None
    )
    after_avg = (
        sum(interface.performance_log["after"]) / len(interface.performance_log["after"])
        if interface.performance_log["after"]
        else None
    )

    # Streamlit UI
    st.title("NIC Optimization Dashboard")
    
    # RTT Data Table
    st.subheader("Real-time RTT Data")
    df = pd.DataFrame(interface.control_data)
    if not df.empty:
        st.dataframe(df)

    # RTT Graph
    if not df.empty:
        st.subheader("RTT Performance Over Time")
        fig, ax = plt.subplots()
        for nic in df["nic"].unique():
            df_nic = df[df["nic"] == nic]
            ax.plot(df_nic["timestamp"], df_nic["average"], marker="o", label=nic)
        
        ax.set_xlabel("Time")
        ax.set_ylabel("RTT (ms)")
        ax.legend()
        st.pyplot(fig)

    # Baseline & Optimized RTT
    baseline_text = f"**Baseline RTT:** {round(before_avg, 2)} ms" if before_avg is not None else "**Baseline RTT:** N/A"
    optimized_text = f"**Optimized RTT:** {round(after_avg, 2)} ms" if after_avg is not None else "**Optimized RTT:** N/A"

    st.write(baseline_text)
    st.write(optimized_text)
