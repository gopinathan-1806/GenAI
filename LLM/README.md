# Local LLM on VM with Streamlit UI

This guide explains how to install a lightweight LLM on an Ubuntu VM
using **Ollama**, expose it through a **Streamlit web UI**, and access
it remotely from a browser.

## 1. Architecture

``` text
Browser
   |
   | HTTP
   v
Streamlit UI :8501
   |
   | HTTP (localhost)
   v
Ollama :11434
   |
   v
Local LLM (qwen3:1.7b)
   |
Ubuntu VM
```

The recommended approach is to expose the **Streamlit UI** to users
while keeping Ollama on localhost.

## 2. VM Requirements

Recommended starting point for a lightweight model:

  Resource   Recommendation
  ---------- ----------------------------------------------------
  OS         Ubuntu 22.04/24.04
  CPU        2+ vCPU
  RAM        8 GB+
  Disk       10 GB+ free
  Swap       2--4 GB recommended
  Network    Internet access during installation/model download

Check resources:

``` bash
free -h
nproc
df -h
```

## 3. Install Ollama

Install Ollama:

``` bash
curl -fsSL https://ollama.com/install.sh | sh
```

Check the service:

``` bash
sudo systemctl status ollama
```

Enable/start it if necessary:

``` bash
sudo systemctl enable --now ollama
```

Verify the API:

``` bash
curl http://localhost:11434/api/tags
```

## 4. Download a Lightweight LLM

For this setup, `qwen3:1.7b` is a lightweight starting point:

``` bash
ollama pull qwen3:1.7b
```

Verify:

``` bash
ollama list
```

You can also use:

``` bash
ollama pull qwen2.5:3b
```

The 3B model may provide better responses but requires more compute
resources.

## 4. Install the LLM Model

Ollama is the runtime that manages and serves the LLM. The actual LLM model is downloaded separately and stored locally on the VM.

For this setup, we use **Qwen3 1.7B**, a relatively small model suitable for lightweight CPU-based experimentation.

### Download the model

```bash
ollama pull qwen3:1.7b
```

This downloads the model files to the VM. The model does not require a separate application installer.

### Verify the installed model

```bash
ollama list
```

Expected output will look similar to:

```text
NAME          ID              SIZE
qwen3:1.7b    8f68893c685c    1.4 GB
```

### Start and interact with the model

```bash
ollama run qwen3:1.7b
```

You can then enter prompts interactively:

```text
>>> Explain Kubernetes deployment in simple terms
```

For a one-time prompt:

```bash
ollama run qwen3:1.7b "Explain Kubernetes deployment in simple terms"
```

### Where is the LLM installed?

The model is stored in Ollama's local model directory on the VM. You can inspect Ollama's configuration/environment with:

```bash
ollama show qwen3:1.7b
```

The important distinction is:

```text
Ollama       = LLM runtime/server
qwen3:1.7b   = actual LLM model
Streamlit    = web-based user interface
```

So the complete installation flow is:

```text
Ubuntu VM
   |
   v
Install Ollama
   |
   v
ollama pull qwen3:1.7b
   |
   v
Model stored locally
   |
   v
ollama run qwen3:1.7b
   |
   v
Ollama API :11434
   |
   v
Streamlit UI :8501
```

### Alternative lightweight model

If the VM has limited CPU/RAM and Qwen3 1.7B is still slow, you can try another smaller model available through Ollama.

For example:

```bash
ollama pull qwen2.5:3b
```

Note that a model's size is not the only factor affecting performance. CPU resources, available RAM, prompt length, context size, and generation length can all affect response time.

## 6. Test the LLM

Test directly from the VM:

``` bash
ollama run qwen3:1.7b
```

Or:

``` bash
ollama run qwen3:1.7b "Explain Kubernetes deployment in simple terms"
```

Only proceed to Streamlit after this works successfully.

## 7. Test the Ollama API

``` bash
curl http://localhost:11434/api/chat   -H "Content-Type: application/json"   -d '{
    "model": "qwen3:1.7b",
    "messages": [
      {
        "role": "user",
        "content": "Explain Kubernetes deployment in simple terms"
      }
    ],
    "stream": false
  }'
```

A JSON response confirms that the model can be consumed by the UI.

## 8. Install Python Dependencies

Create the application directory:

``` bash
mkdir -p ~/local-ai
cd ~/local-ai
```

Create a virtual environment:

``` bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

``` bash
pip install --upgrade pip
pip install streamlit requests
```

## 9. Streamlit Application

Create `app.py` and configure it to send requests to:

``` text
http://localhost:11434/api/chat
```

Use the installed model:

``` text
qwen3:1.7b
```

A production-friendly application should: - Keep the Ollama URL
configurable. - Set a sufficiently long request timeout. - Display a
friendly error instead of a Python traceback. - Maintain chat history
using Streamlit session state. - Handle Ollama/API failures gracefully.

Example request logic:

``` python
response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "qwen3:1.7b",
        "messages": messages,
        "stream": False
    },
    timeout=300
)

response.raise_for_status()
answer = response.json()["message"]["content"]
```

## 10. Start the Streamlit UI

Run:

``` bash
streamlit run app.py   --server.address 0.0.0.0   --server.port 8501
```

The application listens on:

``` text
0.0.0.0:8501
```

Check locally:

``` bash
curl http://localhost:8501
```

## 11. Access from Your Laptop

Find the VM IP:

``` bash
hostname -I
```

Open in a browser:

``` text
http://<VM-IP>:8501
```

Example:

``` text
http://10.x.x.x:8501
```

If the VM is protected by a cloud security group/firewall, allow TCP
`8501` from the required client network.

## 12. Security Recommendation

Use this architecture:

``` text
Laptop
   |
   | HTTP/HTTPS
   v
Streamlit :8501
   |
   | localhost
   v
Ollama :11434
   |
   v
Local LLM
```

**Do not expose Ollama port `11434` publicly** unless there is a
specific requirement and suitable authentication/network controls are
implemented.

For an enterprise/internal deployment, consider: - HTTPS - Reverse proxy
such as NGINX - SSO/authentication - Restricted source IPs -
Firewall/security-group rules - Logging and monitoring - Resource limits

## 13. Run Streamlit as a Systemd Service

Create:

``` bash
sudo vi /etc/systemd/system/local-ai.service
```

Example:

``` ini
[Unit]
Description=Local AI Streamlit Application
After=network.target ollama.service
Requires=ollama.service

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/local-ai
ExecStart=/home/ubuntu/local-ai/venv/bin/streamlit run /home/ubuntu/local-ai/app.py --server.address 0.0.0.0 --server.port 8501
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start:

``` bash
sudo systemctl daemon-reload
sudo systemctl enable --now local-ai
```

Check:

``` bash
sudo systemctl status local-ai
```

View logs:

``` bash
sudo journalctl -u local-ai -f
```

## 14. Troubleshooting Read Timeout

If the UI shows:

``` text
requests.exceptions.ReadTimeout:
HTTPConnectionPool(host='localhost', port=11434):
Read timed out
```

This usually means Ollama received the request but the model did not
finish within the HTTP timeout.

Check Ollama:

``` bash
sudo systemctl status ollama
```

Check models:

``` bash
ollama list
```

Test the model directly:

``` bash
time ollama run qwen3:1.7b "Explain Kubernetes deployment in simple terms"
```

Check the API:

``` bash
curl http://localhost:11434/api/tags
```

Also check CPU/memory:

``` bash
free -h
top
```

For a CPU-only VM, generation can be slow. Increase the application
timeout, reduce prompt size, or use a smaller model if necessary.

## 15. Useful Monitoring Commands

``` bash
free -h
nproc
df -h
top
ss -lntp | grep -E '8501|11434'
sudo journalctl -u ollama -f
sudo journalctl -u local-ai -f
```

## 16. DevOps Troubleshooting Assistant -- Next Stage

Once the basic chat application works, it can be extended into a
Kubernetes troubleshooting assistant.

``` text
User
  |
  v
Streamlit UI
  |
  v
LLM / Agent
  |
  +--> Kubernetes API
  |       |
  |       +--> Deployment
  |       +--> ReplicaSet
  |       +--> Pods
  |       +--> Services
  |       +--> Endpoints
  |       +--> Events
  |       +--> Logs
  |
  v
Graphical Dependency View
```

For a request such as:

> "Show me the frontend deployment"

the assistant could retrieve and visualize:

``` text
Frontend Deployment
        |
        v
    ReplicaSet
     /          v        v
  Pod-1    Pod-2
     \      /
      \    /
       v  v
      Service
         |
         v
   Load Balancer
```

This can provide DevOps engineers with a single view of the
application's Kubernetes resources and help identify dependency or
availability issues faster.

## 17. Setup Summary

The complete setup has three primary layers:

1.  **Ollama** -- local LLM runtime.
2.  **qwen3:1.7b** -- lightweight local model.
3.  **Streamlit** -- browser-based interactive UI.

Typical ports:

  Component      Port Recommended exposure
  ----------- ------- -------------------------------------
  Streamlit      8501 Internal users / controlled network
  Ollama        11434 Localhost only

The model remains on the VM, while users interact through the Streamlit
interface.


<img width="1357" height="795" alt="Screenshot 2026-08-28 at 10 35 43 PM" src="https://github.com/user-attachments/assets/a6b59459-16a6-4d57-8783-c7e86bb2141c" />
<img width="1496" height="558" alt="Screenshot 2026-08-28 at 10 05 12 PM" src="https://github.com/user-attachments/assets/a6f27088-3a32-4257-a58c-5d5eef8947c6" />

