import docker
import tarfile
import io
import os
import sys

class UltraSandbox:
    def __init__(self, image="python:3.9-slim"):
        # Try to connect to Docker specifically for Windows if standard env fails
        try:
            self.client = docker.from_env()
            # Test connection immediately
            self.client.ping()
        except Exception as e:
            print(f"⚠️ Standard Docker connection failed: {e}")
            print("🔄 Attempting Windows-specific named pipe connection...")
            try:
                # Explicitly try the default Windows named pipe
                self.client = docker.DockerClient(base_url='npipe:////./pipe/docker_engine')
                self.client.ping()
                print("✅ Connected to Docker via Named Pipe.")
            except Exception as e2:
                print(f"❌ CRITICAL DOCKER ERROR: Could not connect to Docker Daemon.")
                print(f"Details: {e2}")
                print("👉 ACTION REQUIRED: Ensure Docker Desktop is running and the icon is green.")
                raise e2

        self.image = image
        self.container = None

    def start(self):
        """Starts a secure, isolated container."""
        try:
            # Check if image exists locally, if not pull it
            try:
                self.client.images.get(self.image)
            except docker.errors.ImageNotFound:
                print(f"⬇️ Pulling Docker Image {self.image}...")
                self.client.images.pull(self.image)

            self.container = self.client.containers.run(
                self.image,
                command="tail -f /dev/null",
                detach=True,
                mem_limit="512m",
                network_disabled=True,
                working_dir="/app"
            )
            return self.container.id
        except Exception as e:
            print(f"Docker Launch Error: {e}")
            raise e

    def run_code(self, code: str):
        if not self.container:
            raise Exception("Sandbox not active.")

        try:
            tar_stream = io.BytesIO()
            with tarfile.open(fileobj=tar_stream, mode='w') as tar:
                data = code.encode('utf-8')
                info = tarfile.TarInfo(name="script.py")
                info.size = len(data)
                tar.addfile(info, io.BytesIO(data))
            tar_stream.seek(0)
            
            self.container.put_archive("/app", tar_stream)
            exec_result = self.container.exec_run("python script.py")
            
            return {
                "exit_code": exec_result.exit_code,
                "output": exec_result.output.decode("utf-8")
            }
        except Exception as e:
            return {
                "exit_code": -1,
                "output": f"Sandbox Execution Failed: {str(e)}"
            }

    def stop(self):
        if self.container:
            try:
                self.container.remove(force=True)
            except:
                pass