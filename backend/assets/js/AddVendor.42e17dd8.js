import{d as m,k as r,r as x,c as _,h as e,l as u,v as i,a as f,w as h,E as w,o as b,f as y}from"./index.9e85dc32.js";import{a as g}from"./axios.4d564c32.js";import{u as V}from"./store.76a146f9.js";const S={class:"tw-w-full tw-h-full tw-bg-gray-100 tw-flex tw-items-center tw-justify-center tw-pt-4 tw-px-4"},U={class:"tw-w-full tw-h-full tw-bg-gray-50 tw-rounded-xl tw-flex tw-flex-col tw-px-10"},k=e("p",{class:"tw-text-xl"}," Username ",-1),B=e("p",{class:"tw-text-xl"}," Password ",-1),C=e("p",{class:"tw-text-xl"}," User Display Name ",-1),E=e("p",{class:"tw-text-xl"}," Origin Address ",-1),N=e("p",{class:"tw-text-xl"}," Avatar ",-1),A={class:"tw-py-4"},j=m({__name:"AddVendor",setup(D){V();const l=r(""),a=r(""),o=r(""),d=r(""),n=r(""),p=()=>{if(console.log("submit"),l.value==""||a.value==""||o.value==""||d.value==""||n.value==""){w.confirm("Some fields are empty!").then(()=>{}).catch(()=>{});return}g.post("/api/admin/vendors/create",{vendor_username:l.value,vendor_password:a.value,vendor_display_name:o.value,origin_address:d.value,avatar:n.value}).then(v=>{v.data.code==200&&v.data.data.success==1?w.confirm("Submit Success!").then(()=>{l.value="",a.value="",o.value="",d.value="",n.value=""}).catch(()=>{throw new Error("Submit Fail!")}):w.confirm("Submit Fail!").then(()=>{}).catch(()=>{})})};return(v,t)=>{const c=x("el-button");return b(),_("div",S,[e("div",U,[e("div",null,[k,u(e("input",{"onUpdate:modelValue":t[0]||(t[0]=s=>l.value=s),class:"tw-h-8 tw-w-64",style:{border:"2px solid #d2d2d2"}},null,512),[[i,l.value]])]),e("div",null,[B,u(e("input",{"onUpdate:modelValue":t[1]||(t[1]=s=>a.value=s),type:"password",class:"tw-h-8 tw-w-64",style:{border:"2px solid #d2d2d2"}},null,512),[[i,a.value]])]),e("div",null,[C,u(e("input",{"onUpdate:modelValue":t[2]||(t[2]=s=>o.value=s),class:"tw-h-8 tw-w-64",style:{border:"2px solid #d2d2d2"}},null,512),[[i,o.value]])]),e("div",null,[E,u(e("input",{"onUpdate:modelValue":t[3]||(t[3]=s=>d.value=s),class:"tw-h-8 tw-w-64",style:{border:"2px solid #d2d2d2"}},null,512),[[i,d.value]])]),e("div",null,[N,u(e("input",{"onUpdate:modelValue":t[4]||(t[4]=s=>n.value=s),class:"tw-h-8 tw-w-64",style:{border:"2px solid #d2d2d2"}},null,512),[[i,n.value]])]),e("div",A,[f(c,{size:"large",onClick:p},{default:h(()=>[y("Submit")]),_:1})])])])}}});export{j as default};
