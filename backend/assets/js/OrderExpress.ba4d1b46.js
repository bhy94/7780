import{d as w,k as n,r as m,c as x,h as e,l as d,v as i,a as _,w as f,E as a,o as v,f as h}from"./index.9e85dc32.js";import{a as b}from"./axios.4d564c32.js";import{u as g}from"./store.76a146f9.js";const y={class:"tw-w-full tw-h-full tw-bg-gray-100 tw-flex tw-items-center tw-justify-center tw-pt-4 tw-px-4"},S={class:"tw-w-full tw-h-full tw-bg-gray-50 tw-rounded-xl tw-flex tw-flex-col tw-px-10"},E=e("p",{class:"tw-text-xl"}," Order ID ",-1),V=e("p",{class:"tw-text-xl"}," Express Number ",-1),k={class:"tw-py-4"},D=w({__name:"OrderExpress",setup(B){const u=g(),t=n(""),s=n(""),c=()=>{if(console.log("submit"),t.value==""||s.value==""){a.confirm("Some fields are empty!").then(()=>{}).catch(()=>{});return}b.post("/api/vendors/orders/express",{vendor_id:parseInt(u.vendor_id),order_id:parseInt(t.value),express_number:s.value}).then(o=>{if(o.data.code==200&&o.data.data.success==1)a.confirm("Submit Success!").then(()=>{t.value="",s.value=""}).catch(()=>{});else throw new Error("Submit Fail!")}).catch(o=>{a.confirm("Submit Fail!").then(()=>{}).catch(()=>{})})};return(o,l)=>{const p=m("el-button");return v(),x("div",y,[e("div",S,[e("div",null,[E,d(e("input",{"onUpdate:modelValue":l[0]||(l[0]=r=>t.value=r),class:"tw-h-8 tw-w-64",style:{border:"2px solid #d2d2d2"}},null,512),[[i,t.value]])]),e("div",null,[V,d(e("input",{"onUpdate:modelValue":l[1]||(l[1]=r=>s.value=r),class:"tw-h-8 tw-w-64",style:{border:"2px solid #d2d2d2"}},null,512),[[i,s.value]])]),e("div",k,[_(p,{size:"large",onClick:c},{default:f(()=>[h("Submit")]),_:1})])])])}}});export{D as default};
