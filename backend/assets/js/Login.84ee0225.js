import{d as _,u as f,k as c,r as h,c as v,h as t,l as r,v as u,a as m,w as g,i as n,o as k,f as y,E as p}from"./index.9e85dc32.js";import{a as V}from"./axios.4d564c32.js";const b={class:"tw-w-screen tw-h-screen tw-flex-row tw-bg-gray-100 tw-flex tw-justify-center tw-items-center"},L={class:"tw-bg-gray-50 tw-rounded-2xl tw-flex tw-flex-col tw-items-center tw-justify-center",style:{width:"300px",height:"400px"}},B=t("p",{class:"tw-text-xl"}," Vendor Login ",-1),C={class:"tw-rounded-2xl tw-text-xl tw-p-6"},U={class:"tw-rounded-2xl tw-text-xl"},E={class:"tw-p-4"},P=_({__name:"Login",setup(N){const d=f(),o=c(""),s=c(""),l=e=>{e?p.confirm("Login Success!").then(()=>{d.push("/panel/"),window.location.href="/panel/"}).catch(()=>{d.push("/panel/"),window.location.href="/panel/"}):p.confirm("Login Fail!").then(()=>{}).catch(()=>{})},w=()=>{console.log(o.value),console.log(s.value),V.post("/api/login",{username:o.value,password:s.value,destination:"back_end"}).then(e=>{console.log(e),e.data.code==200&&e.data.data.success==1?(n.set("token",e.data.data.token,{expires:30}),n.set("vendor_username",o.value,{expires:30}),n.set("vendor_id",e.data.data.vendor_id,{expires:30}),n.set("role",e.data.data.role,{expires:30}),l(!0)):l(!1)}).catch(e=>{console.log(e),l(!1)})};return(e,a)=>{const x=h("el-button");return k(),v("div",b,[t("div",L,[B,t("div",C,[r(t("input",{"onUpdate:modelValue":a[0]||(a[0]=i=>o.value=i),type:"text",placeholder:"Username"},null,512),[[u,o.value]])]),t("div",U,[r(t("input",{"onUpdate:modelValue":a[1]||(a[1]=i=>s.value=i),type:"password",placeholder:"Password"},null,512),[[u,s.value]])]),t("div",E,[m(x,{onClick:w},{default:g(()=>[y("Login")]),_:1})])])])}}});export{P as default};
