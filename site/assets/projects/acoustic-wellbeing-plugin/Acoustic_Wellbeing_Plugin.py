# -*- coding: utf-8 -*-
# STATIC noise field + Sleep & Mental Health simulation
# 直达 + 一次反射 + TL + 材料吸声 + 同侧约束
# 源强输入：每个声源点对应一个 float 声级值（Lp0, dB，参考距离 r0 处）
#
# 输出：
#   meshHeat   —— 噪声 dB 绝对色标（蓝→绿→黄→红）
#   meshSleep  —— Sleep Disturbance Index 单色热力图（浅蓝→深蓝）
#   meshMental —— Mental Health Index 单色热力图（浅红→深红）
#   SleepIndex —— 每个格点的 Sleep Disturbance Index（0–1）
#   MentalIndex—— 每个格点的 Mental Health Index（0–1）

import Rhino
import Rhino.Geometry as rg
import Rhino.Geometry.Intersect as rgi
import scriptcontext as sc
import System, math
from datetime import datetime
import System.Drawing as SD

# -------------------------------------------------
# helpers（IronPython 2.7 safe）
# -------------------------------------------------
def _isfinite(x):
    try:
        return (not math.isnan(x)) and (not math.isinf(x))
    except:
        return False

def ensure_list(x):
    if x is None: return []
    if isinstance(x, (list, tuple)): return list(x)
    return [x]

def flatten1(x):
    if isinstance(x, (list, tuple)):
        out = []
        for it in x:
            if isinstance(it, (list, tuple)):
                out.extend(list(it))
            else:
                out.append(it)
        return out
    return [x]

def scalarf(x, default=0.0):
    if isinstance(x, (list, tuple)):
        if len(x) == 0: return float(default)
        return float(scalarf(x[0], default))
    try:
        return float(x)
    except:
        return float(default)

tol = sc.doc.ModelAbsoluteTolerance

def guid_to_curve(obj):
    if isinstance(obj, rg.Curve): return obj
    if isinstance(obj, System.Guid):
        robj = sc.doc.Objects.Find(obj)
        if robj:
            geo = robj.Geometry
            if isinstance(geo, rg.Curve): return geo
            if isinstance(geo, rg.Brep):
                crvs = [e.ToNurbsCurve() for e in geo.DuplicateEdgeCurves(True)]
                j = rg.Curve.JoinCurves(crvs, tol)
                if j and len(j) > 0: return j[0]
    return None

def curve_to_polyline(crv):
    if isinstance(crv, rg.PolylineCurve):
        return crv
    try:
        pl = crv.ToPolyline(0.01, 0.0, 0.0, 0.0)
        if pl and pl.IsValid:
            return pl
    except:
        pass
    try:
        nurbs = crv.ToNurbsCurve()
        pl2 = nurbs.ToPolyline(0.01, 0.0, 0.0, 0.0)
        if pl2 and pl2.IsValid:
            return pl2
    except:
        pass
    return crv

def polyline_points(pl, step_len):
    try:
        if isinstance(pl, rg.PolylineCurve):
            poly = rg.Polyline()
            if pl.TryGetPolyline(poly):
                return [rg.Point3d(p.X, p.Y, 0.0) for p in poly]
    except:
        pass
    try:
        plc = pl.ToPolyline(0.01, 0.0, 0.0, 0.0)
        if isinstance(plc, rg.PolylineCurve):
            poly = rg.Polyline()
            if plc.TryGetPolyline(poly):
                return [rg.Point3d(p.X, p.Y, 0.0) for p in poly]
    except:
        pass
    try:
        tparams = pl.DivideByLength(max(step_len, tol*10), True)
        if tparams:
            return [pl.PointAt(t) for t in tparams]
    except:
        pass
    try:
        return [pl.PointAtStart, pl.PointAtEnd]
    except:
        return []

def poly_contains(pt, crv, pln):
    res = crv.Contains(pt, pln, tol)
    return (res == Rhino.Geometry.PointContainment.Inside) or \
           (res == Rhino.Geometry.PointContainment.Coincident)

def derive_Lp0(L_meas, r_meas, r0):
    return L_meas + 20.0 * math.log10(max(r_meas,1e-6)/max(r0,1e-6))

def Lp_freefield(Lp0, r0, r, alpha_air):
    r = max(r, 0.30)
    return Lp0 - 20.0 * math.log10(r / max(r0,1e-6)) - alpha_air * r

def reflect_point(A,B,S):
    ax,ay=A.X,A.Y; bx,by=B.X,B.Y; sx,sy=S.X,S.Y
    dx,dy = bx-ax, by-ay
    den = dx*dx + dy*dy
    if den == 0: return None, None
    t = ((sx-ax)*dx + (sy-ay)*dy) / den
    px = ax + t*dx; py = ay + t*dy
    rx = 2*px - sx; ry = 2*py - sy
    return rg.Point3d(rx,ry,0.0), t

def line_line_point(P0,P1,Q0,Q1):
    la = rg.Line(P0,P1)
    lb = rg.Line(Q0,Q1)
    rc,ta,tb = rgi.Intersection.LineLine(la,lb)
    if not rc: return None,None,None
    X = la.PointAt(ta)
    return X, ta, tb

def seg_intersects(A,B,C,D,eps=1e-6):
    X,ta,tb = line_line_point(A,B,C,D)
    if X is None: return False
    return (0.0-eps <= ta <= 1.0+eps) and (0.0-eps <= tb <= 1.0+eps)

def wall_normal(A,B):
    vx,vy = (B.X-A.X, B.Y-A.Y)
    n = rg.Vector3d(-vy, vx, 0.0)
    if n.IsTiny(): return rg.Vector3d(0,0,1)
    n.Unitize()
    return n

def same_side(A,B,P,Q):
    vAB = rg.Vector3d(B.X-A.X, B.Y-A.Y, 0.0)
    vAP = rg.Vector3d(P.X-A.X, P.Y-A.Y, 0.0)
    vAQ = rg.Vector3d(Q.X-A.X, Q.Y-A.Y, 0.0)
    z1 = vAB.X*vAP.Y - vAB.Y*vAP.X
    z2 = vAB.X*vAQ.Y - vAB.Y*vAQ.X
    return z1 * z2 >= 0.0

def angle_loss_dB(n, vin):
    eps = 1e-3
    try:
        vn = rg.Vector3d(vin)
        vn.Unitize()
        c = abs(rg.Vector3d.Multiply(n, vn))
        c = max(c, eps)
        return -10.0 * math.log10(c)
    except:
        return 0.0

def material_reflection_loss_dB(alpha):
    a = min(max(alpha,0.0), 0.999)
    return -10.0 * math.log10(max(1.0-a, 1e-6))

def count_crossings_and_TL(P,Q,walls,ignore_idx=-1):
    cnt = 0
    TLsum = 0.0
    for i,(A,B,alpha,TLdB) in enumerate(walls):
        if i == ignore_idx: continue
        if seg_intersects(P,Q,A,B):
            cnt += 1
            TLsum += TLdB
    return cnt, TLsum

def box_blur_once(Lp, idx_map, nx, ny):
    out = Lp[:]
    nbh = [(-1,-1), (0,-1), (1,-1),
           (-1, 0), (0, 0), (1, 0),
           (-1, 1), (0, 1), (1, 1)]
    for iy in range(1, ny-1):
        for ix in range(1, nx-1):
            gi0 = idx_map[iy][ix]
            if gi0 < 0: continue
            ids = []
            for dx,dy in nbh:
                gi = idx_map[iy+dy][ix+dx]
                if gi >= 0: ids.append(gi)
            if len(ids) >= 5:
                s = 0.0
                for gi in ids: s += Lp[gi]
                out[gi0] = s / len(ids)
    return out

def _has(name):
    return name in globals()

# -------------------------------------------------
# 归一化 GH 输入
# -------------------------------------------------
wallAlpha = [scalarf(v,0.1) for v in flatten1(wallAlpha)]
wallTL    = [scalarf(v,30.0) for v in flatten1(wallTL)]
r0         = scalarf(r0,1.0)
r_meas     = scalarf(r_meas,1.0)
cell       = scalarf(cell,0.3)
A_wall_min = scalarf(A_wall_min,0.0)
alpha_air  = scalarf(alpha_air,0.0)

doReflect = bool(doReflect) if _has("doReflect") else False
useBlur   = bool(useBlur)   if _has("useBlur")   else False

absMin_val = scalarf(absMin, 40.0) if _has("absMin") else 40.0
absMax_val = scalarf(absMax, 90.0) if _has("absMax") else 90.0

srcPts   = [pt for pt in flatten1(srcPts)]
srcVals  = [scalarf(v, 60.0) for v in flatten1(srcVals)]

if len(srcPts) != len(srcVals):
    raise ValueError("srcPts 与 srcVals 数量需一致（一个声源点对应一个声级值）。")

# -------------------------------------------------
# 几何预处理
# -------------------------------------------------
outlineCrv = outlineCrv if isinstance(outlineCrv, rg.Curve) else guid_to_curve(outlineCrv)
if outlineCrv is None:
    raise ValueError("outlineCrv 为空或无法转换为 Curve。")
if not outlineCrv.IsClosed:
    raise ValueError("outlineCrv 必须闭合。")

outline_pl = curve_to_polyline(outlineCrv)
ok_pln, outline_pln = outline_pl.TryGetPlane()
if not ok_pln:
    outline_pln = rg.Plane.WorldXY

wallCrvs = ensure_list(wallCrvs)
if len(wallAlpha) == 0: wallAlpha = [0.1]
if len(wallTL)    == 0: wallTL    = [30.0]
if len(wallAlpha) == 1 and len(wallCrvs) > 1:
    wallAlpha = wallAlpha * len(wallCrvs)
if len(wallTL) == 1 and len(wallCrvs) > 1:
    wallTL = wallTL * len(wallCrvs)

walls = []
for i,w in enumerate(wallCrvs):
    cw = w if isinstance(w, rg.Curve) else guid_to_curve(w)
    if not cw: continue
    pl = curve_to_polyline(cw)
    pts = polyline_points(pl, min(0.1, cell*0.4))
    a  = wallAlpha[i] if i < len(wallAlpha) else wallAlpha[-1]
    tl = wallTL[i]    if i < len(wallTL)    else wallTL[-1]
    for k in range(len(pts)-1):
        A = rg.Point3d(pts[k].X,  pts[k].Y,  0.0)
        B = rg.Point3d(pts[k+1].X,pts[k+1].Y,0.0)
        if A.DistanceTo(B) > tol*1e-2:
            walls.append((A,B,a,tl))

# -------------------------------------------------
# 源级
# -------------------------------------------------
Lp0_list = [float(v) for v in srcVals]
timeLabel = "Lp0 input (dB)"

# -------------------------------------------------
# 网格
# -------------------------------------------------
bb = outline_pl.GetBoundingBox(True)
minx, miny = bb.Min.X, bb.Min.Y
maxx, maxy = bb.Max.X, bb.Max.Y

xs = []
x = minx
while x <= maxx + 1e-9:
    xs.append(x)
    x += cell

ys = []
y = miny
while y <= maxy + 1e-9:
    ys.append(y)
    y += cell

gridPts = []
for yy in ys:
    for xx in xs:
        p = rg.Point3d(xx,yy,0.0)
        if poly_contains(p, outline_pl, outline_pln):
            gridPts.append(p)

nx = len(xs)
ny = len(ys)

idx_map = [[-1]*nx for _ in range(ny)]
idx = 0
for iy in range(ny):
    for ix in range(nx):
        p = rg.Point3d(xs[ix],ys[iy],0.0)
        if poly_contains(p, outline_pl, outline_pln):
            idx_map[iy][ix] = idx
            idx += 1

# -------------------------------------------------
# 声场：直达 + 一次反射
# -------------------------------------------------
ener = [0.0] * len(gridPts)

# 直达声
for (S, Lp0i) in zip(srcPts, Lp0_list):
    S2 = rg.Point3d(S.X,S.Y,0.0)
    for k,P in enumerate(gridPts):
        r  = P.DistanceTo(S2)
        Ld = Lp_freefield(Lp0i, r0, r, alpha_air)
        _, TLsum = count_crossings_and_TL(S2, P, walls, ignore_idx=-1)
        Ld_eff = Ld - TLsum
        ener[k] += 10.0**(Ld_eff/10.0)

# 一次反射
if doReflect and walls:
    for wi,(A,B,alpha,TLdB_wall) in enumerate(walls):
        n = wall_normal(A,B)
        for (S, Lp0i) in zip(srcPts, Lp0_list):
            S2 = rg.Point3d(S.X,S.Y,0.0)
            for k,P in enumerate(gridPts):
                if not same_side(A,B,S2,P):
                    continue
                R,_ = reflect_point(A,B,S2)
                if R is None: continue
                I,ta,tb = line_line_point(R,P,A,B)
                if I is None: continue
                if not (0.0-1e-6 <= tb <= 1.0+1e-6 and 0.0-1e-6 <= ta <= 1.0+1e-6):
                    continue
                if count_crossings_and_TL(S2, I, walls, ignore_idx=wi)[0] > 0:
                    continue
                _, TL_after = count_crossings_and_TL(I, P, walls, ignore_idx=wi)
                r_tot = S2.DistanceTo(I) + I.DistanceTo(P)
                Lfree = Lp_freefield(Lp0i, r0, r_tot, alpha_air)
                vin   = rg.Vector3d(I.X-S2.X, I.Y-S2.Y, 0.0)
                A_mat = material_reflection_loss_dB(alpha)
                A_ang = angle_loss_dB(n, vin)
                Lr = Lfree - (A_mat + A_ang + A_wall_min + TL_after)
                ener[k] += 10.0**(Lr/10.0)

# Lp(dB)
Lp = [10.0 * math.log10(max(e, 1e-30)) for e in ener]

if useBlur:
    Lp = box_blur_once(Lp, idx_map, nx, ny)

Lp_vis = Lp[:]

# -------------------------------------------------
# 颜色映射
# -------------------------------------------------
def lerp_color(c1, c2, t):
    t = max(0.0, min(1.0, t))
    r = int(c1.R + (c2.R - c1.R) * t)
    g = int(c1.G + (c2.G - c1.G) * t)
    b = int(c1.B + (c2.B - c1.B) * t)
    return SD.Color.FromArgb(r, g, b)

# 噪声用多色
col_blue   = SD.Color.FromArgb(0, 0, 255)
col_green  = SD.Color.FromArgb(0, 255, 0)
col_yellow = SD.Color.FromArgb(255, 255, 0)
col_red    = SD.Color.FromArgb(255, 0, 0)

def color_map_abs(L):
    if L <= absMin_val:
        return col_blue
    if L >= absMax_val:
        return col_red
    mid = 0.5 * (absMin_val + absMax_val)
    if L <= mid:
        t = (L - absMin_val) / max((mid - absMin_val), 1e-6)
        return lerp_color(col_blue, col_green, t)
    else:
        t = (L - mid) / max((absMax_val - mid), 1e-6)
        return lerp_color(col_yellow, col_red, t)

# Sleep / Mental 用单色渐变
def color_map_sleep(v):
    # v in [0,1] → 浅蓝 → 深蓝
    v = max(0.0, min(1.0, v))
    b = int(50 + 205 * v)
    return SD.Color.FromArgb(0, 0, b)

def color_map_mental(v):
    # v in [0,1] → 浅红 → 深红
    v = max(0.0, min(1.0, v))
    r = int(50 + 205 * v)
    return SD.Color.FromArgb(r, 0, 0)

# -------------------------------------------------
# 噪声 Mesh（原有）
# -------------------------------------------------
meshHeat = rg.Mesh()
vmap = [[-1]*nx for _ in range(ny)]

for iy in range(ny):
    for ix in range(nx):
        gi = idx_map[iy][ix]
        if gi >= 0:
            vmap[iy][ix] = meshHeat.Vertices.Add(xs[ix], ys[iy], 0.0)

for iy in range(ny-1):
    for ix in range(nx-1):
        v00 = vmap[iy][ix]
        v10 = vmap[iy][ix+1]
        v01 = vmap[iy+1][ix]
        v11 = vmap[iy+1][ix+1]
        if v00 >= 0 and v10 >= 0 and v01 >= 0 and v11 >= 0:
            meshHeat.Faces.AddFace(v00, v10, v11, v01)

meshHeat.Normals.ComputeNormals()
meshHeat.VertexColors.CreateMonotoneMesh(SD.Color.Black)

for iy in range(ny):
    for ix in range(nx):
        gi = idx_map[iy][ix]
        vi = vmap[iy][ix]
        if vi >= 0 and gi >= 0:
            L = Lp[gi]
            meshHeat.VertexColors[vi] = color_map_abs(L)

# -------------------------------------------------
# Sleep Disturbance & Mental Health indices
# -------------------------------------------------
baseline_L = 30.0  # dB, 安静基准

SE_max  = 3.3   # %，约等于 Q4-Q1 的 SE 差
SOL_max = 10.0  # min
WASO_max = 10.0 # min
FI_max  = 0.1   # log-unit

def _clip01(x):
    if x < 0.0: return 0.0
    if x > 1.0: return 1.0
    return x

SDI_SE_list = []
SDI_SOL_list = []
SDI_WASOFI_list = []
SDI_list = []
MHI_list = []

for L in Lp:
    dL = max(0.0, L - baseline_L)

    dSE   = 0.19 * dL          # % loss
    dSOL  = 0.5  * dL          # min, 近似
    dWASO = 0.66 * dL          # min
    dFI   = 0.01 * dL          # log-unit

    se_norm   = _clip01(dSE   / SE_max)   if SE_max  > 0 else 0.0
    sol_norm  = _clip01(dSOL  / SOL_max)  if SOL_max > 0 else 0.0
    waso_norm = _clip01(dWASO / WASO_max) if WASO_max> 0 else 0.0
    fi_norm   = _clip01(dFI   / FI_max)   if FI_max  > 0 else 0.0

    sdi_waso_fi = (waso_norm + fi_norm) / 2.0
    sdi_se  = se_norm
    sdi_sol = sol_norm

    # 总 Sleep Disturbance Index（等权）
    sdi = (sdi_waso_fi + sdi_sol + sdi_se) / 3.0

    # Mental Health Index（加权：夜间中断权重更高）
    mhi = 0.4 * sdi_waso_fi + 0.3 * sdi_sol + 0.3 * sdi_se

    SDI_SE_list.append(sdi_se)
    SDI_SOL_list.append(sdi_sol)
    SDI_WASOFI_list.append(sdi_waso_fi)
    SDI_list.append(sdi)
    MHI_list.append(mhi)

# -------------------------------------------------
# Sleep Disturbance Mesh
# -------------------------------------------------
meshSleep = rg.Mesh()
vmap_sleep = [[-1]*nx for _ in range(ny)]

for iy in range(ny):
    for ix in range(nx):
        gi = idx_map[iy][ix]
        if gi >= 0:
            vmap_sleep[iy][ix] = meshSleep.Vertices.Add(xs[ix], ys[iy], 0.0)

for iy in range(ny-1):
    for ix in range(nx-1):
        v00 = vmap_sleep[iy][ix]
        v10 = vmap_sleep[iy][ix+1]
        v01 = vmap_sleep[iy+1][ix]
        v11 = vmap_sleep[iy+1][ix+1]
        if v00 >= 0 and v10 >= 0 and v01 >= 0 and v11 >= 0:
            meshSleep.Faces.AddFace(v00, v10, v11, v01)

meshSleep.Normals.ComputeNormals()
meshSleep.VertexColors.CreateMonotoneMesh(SD.Color.Black)

for iy in range(ny):
    for ix in range(nx):
        gi = idx_map[iy][ix]
        vi = vmap_sleep[iy][ix]
        if vi >= 0 and gi >= 0:
            v = SDI_list[gi]
            meshSleep.VertexColors[vi] = color_map_sleep(v)

# -------------------------------------------------
# Mental Health Mesh
# -------------------------------------------------
meshMental = rg.Mesh()
vmap_mental = [[-1]*nx for _ in range(ny)]

for iy in range(ny):
    for ix in range(nx):
        gi = idx_map[iy][ix]
        if gi >= 0:
            vmap_mental[iy][ix] = meshMental.Vertices.Add(xs[ix], ys[iy], 0.0)

for iy in range(ny-1):
    for ix in range(nx-1):
        v00 = vmap_mental[iy][ix]
        v10 = vmap_mental[iy][ix+1]
        v01 = vmap_mental[iy+1][ix]
        v11 = vmap_mental[iy+1][ix+1]
        if v00 >= 0 and v10 >= 0 and v01 >= 0 and v11 >= 0:
            meshMental.Faces.AddFace(v00, v10, v11, v01)

meshMental.Normals.ComputeNormals()
meshMental.VertexColors.CreateMonotoneMesh(SD.Color.Black)

for iy in range(ny):
    for ix in range(nx):
        gi = idx_map[iy][ix]
        vi = vmap_mental[iy][ix]
        if vi >= 0 and gi >= 0:
            v = MHI_list[gi]
            meshMental.VertexColors[vi] = color_map_mental(v)

# -------------------------------------------------
# GH 输出
# -------------------------------------------------
meshHeat    = meshHeat      # 噪声 dB Mesh
meshSleep   = meshSleep     # Sleep Disturbance Index Mesh (0-1, 单色蓝)
meshMental  = meshMental    # Mental Health Index Mesh (0-1, 单色红)

gridPts     = gridPts
Lp          = Lp
Lp_vis      = Lp_vis
SleepIndex  = SDI_list
MentalIndex = MHI_list
timeLabel   = timeLabel
