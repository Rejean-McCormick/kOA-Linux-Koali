# -*- coding: utf-8 -*-
from pathlib import Path
from datetime import datetime
import base64, hashlib, os, shutil, tkinter as tk, zlib
from tkinter import filedialog, messagebox

REL = "scripts/bootstrap-koali.ps1"
EXPECTED_OLD = "7900ad7e7f06d6d26d7af6db0e5f75c301798f27a49e19c34582068eca893801"
EXPECTED_NEW = "49ea707bca8e192f573f913070502916cd9d1597167d403b8ba71d6c1c795cb0"
PAYLOAD = 'c-qAp+fw63_T696<+vidf)pUx)RrkyLx9PUfq}(jvQ?NOvedRUNNSB*vT-K-&+a$u!#?DL_80b?(=Dkb%Uo(_cX=>&>)iWXTm7$p{4;S=H|lp7yOzr!^X50b!#Vfv&f{>kWv;#xC$Y@jFzgIEo!)VpiuAzC0uf)Ne9BWEdz|evYm|w^>hvyBF-y6WjfX+V<1AbqiZ~16oCDxn;fBGb5E(r0UveqJ1-CEUY|i>Wi6B;Adl#dTmj+2jfR^J}gMoujI=wR>=JQ99D;9t`Hjzh}n{my21Hv7Cw|%}CPhdf2sSE18<4gM_;}N6Jt5w3;QIK*k6X}ZCuSE*#YFZVG-`RPd+3#|&Ag$(-AZnZ|XscvrO9FO2ND+g<PQ~oG5{F_YUnFcn+Y}Yn*5xb!`-Yen`-=5{<e7a0IuPN=1$kERcXsCc_M10RB&9U~Fv|hatU;%DmAbK{odwO)jQhZ*H+4hFI~hp#iP5rMff<t07cGA!@E&U?nx#2s56pAHnSt&@2W4iTz{7t@gN)m6gamcE*JMdnYIVb2A6y-r4%w&ehc2_Htas}i-+Mek&v(wi!`&GlkQjWHiahoYMJQ5s$^EBEgAokETBQNt1yj~vS7QKj7giC8X_QKRQ$<jcF@7IpY^U=8A-jOslVFSM(Mp0RI3Q`rDTJl-Bae9+c+P1cvuiQ=0P8n5!(q&qeF*ny9upipfPEx7{cF%6h-Z)&+=y?n@+Wz)@%xBpZV(R0(pm%usPwNB>E$vLk!JSl6N`b;KGEA_==1P{sO>SIi0o@(>|yY<ZNaQy+nonyvroI)!X&Deun-I^Q>k~!r;xPf%Ew6J$o1wyjQQpII9>#)h$Bz|ECY^iEWCHqz@3D=Zy~C+Wt}NJ3nlI4lBX}G@G~GObRI8;It2UuLZU6A3ZC}?qLNvAR$Y@fuCxzD6uGfq-zs#XlxKMwvtEo2V}o`Swi;ZSiP=VmXU)7lU?#7Vcp>h%{m#vT1>fKp*EdjC6oZ3wCJhHUT>AS}{!)%|k;5jO3h-p4k07u}t`Gki`%=sJ%AiOOC~i&<MpwswJ-IqOKRPDuwkdGtsaUeELd2kev;dWD&O9t1HKZ;D&I6kUF_b%uw+jfjQk;jHp??7-z<9bgR@$HVN)-~Rtewn;+)x!*Q?L`C1roOAV-CsLXOlc*ZVvGQOg$DTbR__Q`GG`d@s+5^!;Uc>8{5vTC5h(ndvL=?I3a8WijVTxT|jIg2gRVa!!^R}Ro~LWfzR4@;9Fb30KRhi?RuCiZ7Fg{)3yse0Y`6_=EKDG?jVacpGtB%3IQ`N(fXD7(Q!v}clS@<z2Wzj^<M)nB~ul}u*}`aNPQ>g4uU`wo+muM<gVYZa0p}WV%5M1skxqhP|z81FNZv|at_l~l0nPkCi9gudUF5*0r5j%oALfYp-xsA$NY;lAo)f~o^jZ)d0)$?z;tl-3l={F8HC+}Lj_2I<dqnaj(tTATA53pgsumP!?w1VMfNg$w~C80+L1r{1Icj|$V5nxkv6)tRke=fY95a!hxQJ$_G@&6Gy!>xf`B%x#XW|c)H?y)=JRThrdHM<#->nWA@`vs7{ieDOv*re3L98&Q`9Gdmu9%)GSg2HzCdQ|3wE#&flun8E8xxynH0bZV%!%?`SpcZ@^m!kU`I0`AshvR@GA*n+}fdVeF!<uBH`yCST=`lh~Fmy4G?4wbKV_aG36>4bZ)qGSMaZhJV%r3%|Q@QtLEuS_yU5AN>#PnQ$-YUy2_s@mvt(?(p#YFM)%jaONHYL_73yl_xroMC=ALC-ht_18Vbl+6YjZCaM*b|6GiGEH9EZ*5YO+b#tp4p%R>mDvXJtD)LmjJ`;rw8m~Df9OEBfYxk`hmul`Zn)3+9?3P$b+K~)r-?WT`JoKX@6000gB_4W+`RkA2>d&b%BE+|;0NDYGiUr*i4!c_3n$U#HEztgLc#SFwvI#rp~LQH7WODh_Al(|!gUzVg|5ul>L8mW^s@0IRP*@Q&V+8byMQ#Fjj>@Wih80o(zWKjh6Ai8p_{RUx7{bj$WG`5%pG3c+X8X$U45+@O=Tq+2j12GbSPf=~RBwIqFBvVjt2PI6;APzgC@L_2l1EpU*h;u9njK>K6>yUwM04Mg{)GuODxobTNDZ<<g(n<mjo(Ul4Q33{64kFwRAGY9dIHutg>H&ti9HS;+58T!%?3SdqKtTEBAzu(_aPkY#Ppf-b6iyguceb6~ZD-q309QhU>$90L(`5i4$7m~!flWnNI8{A$ne@o`w<?jyu`>x`BI0<F4}{bZFhq=slqy|~tX(NlrE86%V$&#e3pdQU^2q|G@=3P)JuxVKb3^yVKdSDl=r|Qo)m~Mj7^`)pn2s8mx@jt%NIdu&_+Z^Cf*NYBqZTdM8ZOG(w#}+iwwict2OkRARjO&hvhkyyO3IxaXtidcn7AQgq4~|$+<<jP)KWdy3>D4KX#hjgCsjAv;j;f#?Qq#08(E6-No&+Kn`HQn9L>ZN;+}-7N1J2Q=tch4Yc&>`s7R|+W)peJcouPZ!2wGxs*O{YwHCV&ui0NGDW3-S&|{mFw#Zzs+RW8Oq*&N)?gyEre?U_3twGH;j|H2tEvKdGlvCN#Rn}K|)*r58t4(-j0HF`{62os>Jb9fGxm^v7y4($}{1OK%%c4QNQ5KaO6lJkn6QghV%O2RNswgFgLASH1#mE;`gVAhNTs-9nZ8>-H#UovcNkaR0zIa||VyK8L3I+R64iwe(24!F-0CUD&cW*5idUvvdY8!)VR&M@{v$L!IeWU(;OWtZ)osewk7_tCHfJ#2X-C~GJpWiaD1PqsuD^?)5RhwjvW0|KQ6ckrI&}=-`stq+ay)z=3RynO1Mg8U!V(BSY9perLYiAPXa~1_s0;8cq)-j~(f6Itd>klk7@w!n`hb+*G6XMzdbCeL;v>ND&*jt<QG*8?*Q>CrqC;Izcxd!2&7FKSAdyBv29O&FFfwi{AT45L%gX>y?(u$A?E1ytSw6x`{x=olnk$9M}S9BU`*j>Xeyr_l?Ik$$a2dW;7{wXIzHQE)jCrYPkcbp-VeF<Za2>>k+hj|IWEUQteT9j3#QnS<nr}CV!XGI{IW50G)D(@;=p=9-VY)j9L!h>Za6~FPAb`z&hprbrN*;4EB%sSRyl4=D1kIu;0$lST(*b_eRWItcM{&Rf~?f2BtnzCy5*yvk6hdI;du@~S3t!$!?;S4HvgzYi+>luq2<2{cT7nA_knt8QsBq|NDIZ<hpf!U?g98XFZ^MLDRIn;hN5GW*Od&~+VJknrtCHI&*37U34!7oQwhua{Y3Wvt=2dCvh5W|D+z-k>S%0r9wu|l=dg;><Q7RuJfi>6Zb^L~k5rEM86o}2y=_Aw(H=0(sV9$Q=@af6i7RX636JP66n0`Rvefe3=~{I&WKau{R5a`6Js!I-vx!MRK1FL@*uT(_d90aSJ9%}XI50pVe#<Yh}*JK@hnq8)d0sYdqDdXo0oi|Wc<>EA03XqzQg$@{`0`=sx-6xmgxcsQAW2yZL1HHh{?OJ;7VvSfd%lS=hE3}IR7Jv9vZ1VN_TP>&V-=PSl_)wgitFxSC1-E7j)x|7{!PZV6kdzBWgg|_H;8?MMmEnPCZRgK$RsM{&1g5A}%;D1_p*Yaz*-=#|y=4vJotz6I8;Q~ix(Moj7((0&b{6&TRk#0IjYOS;prRs}*GvgG+_P<>1);5<{uRNbFeqGEZ>s>mtRM1E$^4R>F*B{j3S{sf?XTqxG41IUR!b9ybet=Od!f&5r9&2u36almPli>{CV!$vAw4UPiuu)EXDbmoFPl$W_i-IboZlea)1aT-C+jl&Td1z;=gsX<Ho&Je|@|IA>29;YyWvpkfu|cgNM=j|yOLFKdv*6BlQ*RE{$=kqwq~PA(9u#on^(Ev*W8zcHw3yI6gF|74%|!ZgzL$#1?YT+i2@&o@JPrJIUT^8ySc5!CDBVOQ9p9CLe7gyM-330!zU#d5r0lL8aX$b?P=t6p<Gb^N+p`L2Y$7~^ei+30{YJ{r3BluW1*j-~V|6+`VpOln&yh(Z(rJvk+4eF5_9S%UyMoNoq%o)0Xj|Jmw?{vq__qcHM}7>!MGF##=tr|h$(YE2UR9lfrg72I(kT0=zGvLl*|d+Wl}Kj)b@s>KNrXTC1~RZh2IeW*t47Q~@9LwiW}nh1``V24Hl^u$cEQm&ETVm268db_c59Ka8jb#f9W?XZ%$>N<EEI<T>QYs+r+JK7bs|w`*W{p&C~!p43^tw#Xno5!-+HeD>MLMOj~Gl3^Dvk&J)I%m9-}8sPx4Ek00;z7NPpwEg;0CU9PiTo7LY#D?&DnNrnANM&dp$p)t7d02_};i-vILc*Eom`ieWKzz_59k!9wZ=ptZUfaC{$R{cTh~b!6^AnU~5aI|Hkw1**9)RAbwNhNra3R$;NN{<?EZ$mo$P$2y|GsOrgDWAh(4RAn~R>Ll0<No==hyzfB_WT^-@CK8>))N%5m0tP6|<c(Klrh)}k-7V>#PO@5-ubTAQ`?Z0m#I0r?z0{T`OfnlLpckC))ff%dqq@??PRIskjA`*O!<&PI_1Gy@LpAW9b&JuBBpy!f3<SmISwGx+TDZbFN_2=$DY<Xy7olaaKW7rDi>fLa*=TJPX_uzl+4`mt9c`n}XPm~V$4l)~Ts<-<P;*Q#RO})F85Ayl#2980#$HbM39wVa_Z^cw_HoX@Qk2i;>KcpB7d#XRjUwiu+#WkZ0%`GTv3wVZCok%vsd@z{@zw?Q5$c9EUQSuN)e1VO3{$<*+JUt^!B?;T0cPxLyfA$QlHLr5KWE-Mv2@B?UY4L?-7DXi0{BFT(72@!kE4~RF2U=hfhDTA?W-@{;tgOe=I=~jD7zB&Px!XMKH>=k-gofikx9_FwB9i;-?rSnReXjfMz^(&_a-jB2Yl5pE+_xaewlOV^3KV8_~QB2QP)Kv+oJCkfexb<pQWx3Ub1E3wGEDK^h0^D0fe1Hk)sx~jP4+iFDkj|;EVMwCHTi2KBs}c-B}&C4H?~NCt4ubYmpwi-n=FnT}1neS^EfCiuzFA%H3iRn=0?%HSAsO(4Xyk_rC#`&Xnx'

MARKERS = [
    "KOALI.pyw",
    "package.json",
    "config/ecosystem.catalog.json",
    "launcher/koali_launcher.py",
]

def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def valid_root(path):
    return all((path / marker).exists() for marker in MARKERS)

def find_root():
    here = Path(__file__).resolve().parent
    candidates = [
        here,
        here.parent / "koali-spaces",
        here.parent.parent / "koali-spaces",
        Path(r"C:\mycode\kOA-Linux\koali-spaces"),
    ]
    seen = set()
    for candidate in candidates:
        try:
            candidate = candidate.resolve()
        except Exception:
            pass
        key = str(candidate).casefold()
        if key in seen:
            continue
        seen.add(key)
        if valid_root(candidate):
            return candidate
    return None

def main():
    app = tk.Tk()
    app.withdraw()

    root = find_root()
    if root is None:
        selected = filedialog.askdirectory(
            title="Choisir la racine koali-spaces",
            initialdir=r"C:\mycode\kOA-Linux",
        )
        if not selected:
            return 1
        root = Path(selected)
        if not valid_root(root):
            messagebox.showerror("Koali SHA256 hotfix", "Racine Koali invalide.")
            return 2

    target = root / REL
    if not target.is_file():
        messagebox.showerror("Koali SHA256 hotfix", f"Fichier absent :\n{target}")
        return 3

    current = digest(target)
    if current == EXPECTED_NEW:
        messagebox.showinfo("Koali SHA256 hotfix", "Le correctif est déjà appliqué.")
        return 0
    if current != EXPECTED_OLD:
        messagebox.showerror(
            "Koali SHA256 hotfix",
            "Aucune modification effectuée.\n\n"
            f"Version inattendue de {REL} :\n{current}\n\n"
            "Le hotfix refuse d'écraser un fichier modifié.",
        )
        return 4

    if not messagebox.askyesno(
        "Koali SHA256 hotfix",
        f"Racine :\n{root}\n\n"
        "Remplacer Get-FileHash par SHA-256 .NET natif ?",
    ):
        return 1

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = root / ".koali-update-backups" / f"sha256-dotnet-{stamp}" / REL
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(target, backup)

    try:
        patched = zlib.decompress(base64.b85decode(PAYLOAD.encode("ascii")))
        if hashlib.sha256(patched).hexdigest() != EXPECTED_NEW:
            raise RuntimeError("Payload corrompu")
        temp = target.with_name(target.name + ".koali-hotfix.tmp")
        temp.write_bytes(patched)
        os.replace(temp, target)
        if digest(target) != EXPECTED_NEW:
            raise RuntimeError("Validation post-écriture échouée")
    except Exception as exc:
        shutil.copy2(backup, target)
        messagebox.showerror(
            "Koali SHA256 hotfix",
            f"Échec; restauration effectuée.\n\n{type(exc).__name__}: {exc}",
        )
        return 5

    messagebox.showinfo(
        "Koali SHA256 hotfix",
        "Correctif appliqué.\n\n"
        "Relance START_KOALI.cmd.\n"
        "Le bootstrap n'utilise plus Get-FileHash.",
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
