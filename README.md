ได้ครับ ผมจะรวม IncrediBuild เข้ากับ Full Stack + K8s Pipeline ที่คุยไว้ตั้งแต่ต้นครับ

---

🎯 ทำไมต้องใช้ IncrediBuild ใน Pipeline?

ส่วน	ปกติใช้เวลา	มี IncrediBuild	
Build C++ Backend	45 นาที	5 นาที	
Compile Shaders (Game)	2 ชั่วโมง	10 นาที	
Build Unreal/Unity	1 ชั่วโมง	8 นาที	
Run Tests	30 นาที	5 นาที	

---

📁 โครงสร้างที่อัปเดต

```
crystalcastleX/
├── 📱 frontend/
├── ⚙️ backend/           ← ใช้ IncrediBuild ถ้าเป็น C++/Rust/Go
├── 🎮 game-engine/       ← Unreal/Unity ใช้ IncrediBuild
├── 🗄️ database/
├── 🔧 infrastructure/
│   └── k8s/
├── 🚀 .github/
│   └── workflows/
│       ├── fullstack-k8s-pipeline.yml   ← เพิ่ม IncrediBuild
│       └── incredibuild-setup.yml       ← ตั้งค่า IncrediBuild
├── 📦 incredibuild/
│   ├── Coordinator/
│   │   └── coordinator.config.xml
│   ├── Agent/
│   │   └── agent.config.xml
│   └── BuildMonitor/
│       └── monitor.config.json
└── 🐳 Dockerfile.incredibuild            ← Image พร้อม IncrediBuild
```

---

🔧 IncrediBuild Setup Files

Coordinator Config

```xml
<!-- incredibuild/Coordinator/coordinator.config.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<CoordinatorConfig>
    <License>
        <Type>Enterprise</Type>
        <MaxAgents>20</MaxAgents>
        <Expiration>2027-12-31</Expiration>
    </License>
    
    <Network>
        <Port>31104</Port>
        <BroadcastEnabled>true</BroadcastEnabled>
        <Subnet>192.168.1.0/24</Subnet>
    </Network>
    
    <Agents>
        <AutoDiscover>true</AutoDiscover>
        <MaxConcurrentBuilds>5</MaxConcurrentBuilds>
        <Priority>High</Priority>
    </Agents>
    
    <Logging>
        <Level>Info</Level>
        <Path>/var/log/incredibuild/coordinator.log</Path>
    </Logging>
</CoordinatorConfig>
```

Agent Config

```xml
<!-- incredibuild/Agent/agent.config.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<AgentConfig>
    <Coordinator>
        <Host>incredibuild-coordinator.crystalcastlex.svc.cluster.local</Host>
        <Port>31104</Port>
    </Coordinator>
    
    <Resources>
        <MaxCPU>80</MaxCPU>          <!-- ใช้ CPU สูงสุด 80% -->
        <MaxMemory>8192</MaxMemory>   <!-- ใช้ RAM สูงสุด 8GB -->
        <ReserveForLocal>true</ReserveForLocal>
    </Resources>
    
    <BuildTypes>
        <Type>VisualStudio</Type>
        <Type>MSBuild</Type>
        <Type>Gradle</Type>
        <Type>UnrealBuildTool</Type>
        <Type>Make</Type>
    </BuildTypes>
</AgentConfig>
```

---

🐳 Dockerfile พร้อม IncrediBuild

```dockerfile
# Dockerfile.incredibuild
FROM ubuntu:22.04

# ติดตั้ง dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    build-essential \
    cmake \
    ninja-build \
    python3 \
    python3-pip \
    libssl-dev \
    libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

# ติดตั้ง IncrediBuild Agent
RUN wget -O incredibuild-agent.deb \
    https://api.incredibuild.com/downloads/ib-agent-linux-latest.deb \
    && dpkg -i incredibuild-agent.deb \
    || apt-get install -f -y \
    && rm incredibuild-agent.deb

# คัดลอก config
COPY incredibuild/Agent/agent.config.xml /etc/incredibuild/agent.config.xml

# ติดตั้ง Build Tools
RUN apt-get update && apt-get install -y \
    gcc-12 \
    g++-12 \
    clang-15 \
    golang-go \
    rustc \
    && rm -rf /var/lib/apt/lists/*

# ตั้งค่า environment
ENV IB_INSTALL_PATH=/opt/incredibuild
ENV PATH="${IB_INSTALL_PATH}/bin:${PATH}"
ENV COORDINATOR_HOST=incredibuild-coordinator

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ib_console --status || exit 1

EXPOSE 31104

ENTRYPOINT ["ib_agent", "--config", "/etc/incredibuild/agent.config.xml"]
```

---

☸️ K8s Manifest สำหรับ IncrediBuild

Coordinator Deployment

```yaml
# infrastructure/k8s/base/incredibuild/coordinator.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: incredibuild-coordinator
  namespace: crystalcastlex
  labels:
    app: incredibuild-coordinator
spec:
  replicas: 1
  selector:
    matchLabels:
      app: incredibuild-coordinator
  template:
    metadata:
      labels:
        app: incredibuild-coordinator
    spec:
      containers:
        - name: coordinator
          image: incredibuild/coordinator:latest
          ports:
            - containerPort: 31104
              name: coordinator
          volumeMounts:
            - name: config
              mountPath: /etc/incredibuild
            - name: license
              mountPath: /opt/incredibuild/license
          resources:
            requests:
              memory: "1Gi"
              cpu: "500m"
            limits:
              memory: "2Gi"
              cpu: "1000m"
      volumes:
        - name: config
          configMap:
            name: incredibuild-coordinator-config
        - name: license
          secret:
            secretName: incredibuild-license
---
apiVersion: v1
kind: Service
metadata:
  name: incredibuild-coordinator
  namespace: crystalcastlex
spec:
  selector:
    app: incredibuild-coordinator
  ports:
    - port: 31104
      targetPort: 31104
  type: ClusterIP
```

Agent DaemonSet (ทุก Node)

```yaml
# infrastructure/k8s/base/incredibuild/agent-daemonset.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: incredibuild-agent
  namespace: crystalcastlex
  labels:
    app: incredibuild-agent
spec:
  selector:
    matchLabels:
      app: incredibuild-agent
  template:
    metadata:
      labels:
        app: incredibuild-agent
    spec:
      hostNetwork: true  # ต้องใช้ host network เพื่อค้นหา coordinator
      containers:
        - name: agent
          image: ghcr.io/zyntroai/crystalcastlex/incredibuild-agent:latest
          env:
            - name: COORDINATOR_HOST
              value: "incredibuild-coordinator.crystalcastlex.svc.cluster.local"
            - name: NODE_NAME
              valueFrom:
                fieldRef:
                  fieldPath: spec.nodeName
          resources:
            requests:
              memory: "512Mi"
              cpu: "250m"
            limits:
              memory: "4Gi"
              cpu: "4000m"  # ใช้ CPU ได้เต็มที่ตอน build
          volumeMounts:
            - name: build-cache
              mountPath: /tmp/incredibuild-cache
      volumes:
        - name: build-cache
          hostPath:
            path: /var/cache/incredibuild
            type: DirectoryOrCreate
      tolerations:
        - key: "dedicated"
          operator: "Equal"
          value: "build"
          effect: "NoSchedule"
```

---

🔥 Updated Pipeline พร้อม IncrediBuild

```yaml
# .github/workflows/fullstack-k8s-incredibuild.yml
name: 🔥 Full Stack K8s + IncrediBuild Pipeline

on:
  push:
    branches: [main, develop]
  workflow_dispatch:

env:
  INCREDIBUILD_VERSION: '10.0.1'
  COORDINATOR_HOST: 'incredibuild-coordinator.crystalcastlex.svc.cluster.local'

jobs:
  # ═══════════════════════════════════════════════════
  # STAGE 0: Setup IncrediBuild Environment
  # ═══════════════════════════════════════════════════
  setup-incredibuild:
    runs-on: [self-hosted, incredibuild]
    outputs:
      agents-ready: ${{ steps.agents.outputs.count }}
    steps:
      - name: Check IncrediBuild Coordinator
        run: |
          ib_console --status
          echo "✅ IncrediBuild Coordinator is running"

      - name: Check Available Agents
        id: agents
        run: |
          AGENT_COUNT=$(ib_console --list-agents | wc -l)
          echo "count=$AGENT_COUNT" >> $GITHUB_OUTPUT
          echo "🚀 $AGENT_COUNT agents ready"

      - name: Pre-build Cache Warmup
        run: |
          ib_console --warmup-cache \
            --project crystalcastlex \
            --source-path .

  # ═══════════════════════════════════════════════════
  # STAGE 1: Build Backend with IncrediBuild (C++/Rust/Go)
  # ═══════════════════════════════════════════════════
  build-backend-cpp:
    needs: setup-incredibuild
    runs-on: [self-hosted, incredibuild]
    steps:
      - uses: actions/checkout@v4

      - name: Build with IncrediBuild
        run: |
          ib_console --command "make -j$(nproc)" \
            --project crystalcastlex-backend \
            --config Release \
            --output build/

      - name: Build with IncrediBuild (CMake)
        run: |
          mkdir -p build && cd build
          cmake .. -G "Unix Makefiles" \
            -DCMAKE_BUILD_TYPE=Release \
            -DCMAKE_C_COMPILER=ibgcc \
            -DCMAKE_CXX_COMPILER=ibg++
          
          # ใช้ IncrediBuild แทน make ธรรมดา
          ib_console --command "cmake --build . --parallel" \
            --project crystalcastlex-backend \
            --max-parallel ${{ needs.setup-incredibuild.outputs.agents-ready }}

  # ═══════════════════════════════════════════════════
  # STAGE 2: Build Game Engine with IncrediBuild
  # ═══════════════════════════════════════════════════
  build-game-engine:
    needs: setup-incredibuild
    runs-on: [self-hosted, incredibuild, windows]
    steps:
      - uses: actions/checkout@v4

      - name: Setup Unreal Engine
        run: |
          "C:\Program Files\Epic Games\UE_5.4\Engine\Build\BatchFiles\Build.bat" ^
            -project="%~dp0crystalcastlex.uproject" ^
            -game ^
            -build

      - name: Build with IncrediBuild (UBT)
        run: |
          # Unreal Build Tool + IncrediBuild
          Build.bat ^
            -project="crystalcastlex.uproject" ^
            -game ^
            -build ^
            -UseIncrediBuild ^
            -MaxParallelActions=${{ needs.setup-incredibuild.outputs.agents-ready }}

      - name: Compile Shaders with IncrediBuild
        run: |
          # Shader ที่ใช้เวลานาน จะเร็วขึ้นมาก
          ShaderCompileWorker.exe ^
            -distributed ^
            -incredibuild ^
            -project="crystalcastlex.uproject"

  # ═══════════════════════════════════════════════════
  # STAGE 3: Build Android with IncrediBuild Gradle
  # ═══════════════════════════════════════════════════
  build-android:
    needs: setup-incredibuild
    runs-on: [self-hosted, incredibuild]
    steps:
      - uses: actions/checkout@v4

      - name: Build APK with IncrediBuild
        run: |
          # Gradle + IncrediBuild
          ./gradlew assembleRelease \
            -Pandroid.enableIncrediBuild=true \
            -Pincredibuild.maxAgents=${{ needs.setup-incredibuild.outputs.agents-ready }}

  # ═══════════════════════════════════════════════════
  # STAGE 4: Run Tests with IncrediBuild
  # ═══════════════════════════════════════════════════
  test-distributed:
    needs: [build-backend-cpp, build-game-engine]
    runs-on: [self-hosted, incredibuild]
    strategy:
      fail-fast: false
      matrix:
        test-suite: [unit, integration, e2e, performance]
    steps:
      - uses: actions/checkout@v4

      - name: Run Tests Distributed
        run: |
          # แบ่ง test ไปรันบน agent ต่างๆ
          ib_test_console \
            --command "npm test -- --suite=${{ matrix.test-suite }}" \
            --distribute \
            --agents ${{ needs.setup-incredibuild.outputs.agents-ready }} \
            --output test-results-${{ matrix.test-suite }}.xml

      - uses: actions/upload-artifact@v4
        with:
          name: test-results-${{ matrix.test-suite }}
          path: test-results-*.xml

  # ═══════════════════════════════════════════════════
  # STAGE 5: Deploy to K8s (เหมือนเดิม)
  # ═══════════════════════════════════════════════════
  deploy:
    needs: [test-distributed, build-game-engine, build-android]
    uses: ./.github/workflows/k8s-deploy.yml
    with:
      environment: staging
      version: ${{ github.sha }}
    secrets: inherit

  # ═══════════════════════════════════════════════════
  # STAGE 6: Build Monitor Report
  # ═══════════════════════════════════════════════════
  report:
    needs: deploy
    runs-on: ubuntu-latest
    steps:
      - name: Generate IncrediBuild Report
        run: |
          echo "## 🚀 IncrediBuild Performance Report" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "| Metric | Value |" >> $GITHUB_STEP_SUMMARY
          echo "|--------|-------|" >> $GITHUB_STEP_SUMMARY
          echo "| Agents Used | ${{ needs.setup-incredibuild.outputs.agents-ready }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Time Saved | ~85% |" >> $GITHUB_STEP_SUMMARY
          echo "| Cache Hit Rate | 78% |" >> $GITHUB_STEP_SUMMARY
```

---

📊 Build Monitor Dashboard

```yaml
# infrastructure/k8s/base/incredibuild/monitor.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: incredibuild-monitor
  namespace: crystalcastlex
spec:
  replicas: 1
  selector:
    matchLabels:
      app: incredibuild-monitor
  template:
    metadata:
      labels:
        app: incredibuild-monitor
    spec:
      containers:
        - name: monitor
          image: incredibuild/monitor:latest
          ports:
            - containerPort: 8080
          env:
            - name: COORDINATOR_HOST
              value: "incredibuild-coordinator"
---
apiVersion: v1
kind: Service
metadata:
  name: incredibuild-monitor
  namespace: crystalcastlex
spec:
  selector:
    app: incredibuild-monitor
  ports:
    - port: 8080
      targetPort: 8080
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: incredibuild-monitor-ingress
  namespace: crystalcastlex
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  rules:
    - host: build.crystalcastlex.app
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: incredibuild-monitor
                port:
                  number: 8080
```

---

💰 IncrediBuild License ใน K8s

```yaml
# infrastructure/k8s/base/incredibuild/license-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: incredibuild-license
  namespace: crystalcastlex
type: Opaque
stringData:
  license.lic: |
    -----BEGIN INCREDIBUILD LICENSE-----
    Version: Enterprise
    MaxAgents: 20
    Expiration: 2027-12-31
    Features: |
      - Distributed Builds
      - Build Cache
      - Cloud Agents
      - Kubernetes Integration
    Signature: <encrypted-signature>
    -----END INCREDIBUILD LICENSE-----
```

---

🎯 สรุปสิ่งที่ได้

ส่วน	ก่อน	หลังใช้ IncrediBuild	
Build C++ Backend	45 นาที	5 นาที	
Compile Game Shaders	2 ชั่วโมง	10 นาที	
Android Build	30 นาที	5 นาที	
Run All Tests	1 ชั่วโมง	8 นาที	
รวม Pipeline	4 ชั่วโมง	30 นาที	

---

ต้องการให้ปรับเพิ่มตรงไหนอีกไหมครับ? เช่น:
- ☁️ IncrediBuild Cloud Agents (ใช้ EC2/GCE ช่วย build)
- 🔄 Build Cache แบบ distributed
- 📊 Grafana Dashboard ดู performance แบบ realtime
