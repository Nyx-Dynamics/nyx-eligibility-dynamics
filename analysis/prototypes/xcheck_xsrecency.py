# Cross-check CEPHIA MDRI using XSRecency's approach: Evaluation Panel, final result, subtypes A1/B/C/D,
# no EDDI-interval filter, logit polynomial in ui (years), GEE clustered by participant (independence).
import pandas as pd, numpy as np, statsmodels.api as sm
d=pd.read_pickle('cephia.pkl')
c=d[(d.cephia_panel=='CEPHIA 1 Evaluation Panel')&(d.assay_result_field=='final_result')&(d.hiv_subtype.isin(['A1','B','C','D']))&d.days_since_eddi.notna()]
l=c[c.assay=='LAg-Sedia'].copy(); l['odn']=pd.to_numeric(l.assay_result_value,errors='coerce')
l=l.dropna(subset=['odn']); l['ui']=l.days_since_eddi/365.25
rng=np.random.default_rng(1)
def run(df,vl,deg,maxfit):
    df=df[(df.ui<=maxfit)&(df.ui>=0)].copy()
    df['ri']=((df.odn<=1.5)&(df.viral_load_closest_to_visit>vl)).astype(int)   # NA VL -> not recent (as XSRecency)
    X=np.column_stack([df.ui**k for k in range(deg+1)])
    m=sm.GEE(df.ri,X,groups=df.participant_identifier,family=sm.families.Binomial(),cov_struct=sm.cov_struct.Independence()).fit()
    uu=np.linspace(0,2,2001); U=np.column_stack([uu**k for k in range(deg+1)])
    om=lambda b: np.trapezoid(1/(1+np.exp(-(U@b))),uu)*365.25
    draws=rng.multivariate_normal(m.params,m.cov_params(),2000)
    o=np.array([om(b) for b in draws])
    return om(np.asarray(m.params)),np.percentile(o,[2.5,97.5]),df.participant_identifier.nunique()
for sub in ['C','B']:
    S=l[l.hiv_subtype==sub]
    for vl in [75,1000]:
        for deg,mx in [(3,800/365.25),(3,5),(4,5)]:
            est,ci,n=run(S,vl,deg,mx)
            print(f'subtype {sub} VL>{vl:4d} logit deg{deg} fit<= {mx:4.1f}y: MDRI {est:5.1f} d (95% {ci[0]:.0f}-{ci[1]:.0f}), {n} participants')
