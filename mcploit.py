from fastmcp import FastMCP
from pymetasploit3.msfrpc import MsfRpcClient  # Import the correct client
from typing import Dict, Any

mcp = FastMCP("Advanced Metasploit Server")

class MetasploitManager:
    def __init__(self):
        self.client = None
        self.connect()
    
    def connect(self):
        """Establish connection to Metasploit RPC"""
        try:
            self.client = msfrpc.Msfrpc({})
            self.client.login('msf', 'myName')  # Update credentials
        except Exception as e:
            print(f"Metasploit connection failed: {e}")
    
    @mcp.tool()
    def list_modules(self, module_type: str = "exploits") -> list:
        """List available Metasploit modules by type (exploits, payloads, auxiliary)"""
        try:
            modules = self.client.call(f'module.{module_type}')
            return modules.get('modules', [])
        except Exception as e:
            return [f"Error listing {module_type}: {str(e)}"]
    
    @mcp.tool()
    def module_info(self, module_path: str) -> Dict[str, Any]:
        """Get detailed information about a specific module"""
        try:
            info = self.client.call('module.info', [module_path])
            return info
        except Exception as e:
            return {"error": f"Failed to get module info: {str(e)}"}
    
    @mcp.tool()
    def check_vulnerability(self, target: str, module: str) -> Dict[str, Any]:
        """Check if a target is vulnerable using a specific module"""
        try:
            # Create a job for vulnerability checking
            result = self.client.call('module.check', [module, target])
            return result
        except Exception as e:
            return {"error": f"Vulnerability check failed: {str(e)}"}

# Initialize the Metasploit manager
msf_manager = MetasploitManager()

if __name__ == "__main__":
    mcp.run(transport='sse', port=9000)

