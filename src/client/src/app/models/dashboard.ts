interface DockerInfo {
  api_version: string
  go_version: string
  platform_name: string
  platform_version: string
}
interface OsInfo {
  type: string
  version: string
  name: string
}

interface ContainersInfo {
  total: number
  paused: number
  running: number
  stopped: number
}

interface SystemWideInfo {
  os: OsInfo
  containers: ContainersInfo
  root_dir: string
  kernel_version: string
  images: number
  cpu_count: number
  total_memory: string
}

export interface DashboardInfo {
  docker_info: DockerInfo
  system_wide_info: SystemWideInfo
}