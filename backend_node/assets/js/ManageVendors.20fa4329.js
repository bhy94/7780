import{d as v,k as h,j as f,r as d,e as w,w as l,E as r,o as b,a,m as g,f as x}from"./index.36428d0e.js";import{a as c}from"./axios.4d564c32.js";import{u as y}from"./store.ef743312.js";const M=v({__name:"ManageVendors",setup(k){const i=y(),_=e=>{c.post("/api/admin/vendors/delete",{user_id:0,vendor_id:parseInt(t.value[e].vendor_id),role:"vendors"}).then(o=>{if(console.log(o),o.data.code==200&&o.data.data.success==1)r.confirm("Delete Order Success!").then(()=>{t.value.splice(e,1)}).catch(()=>{t.value.splice(e,1)});else throw new Error("Delete Order Fail!")}).catch(o=>{console.log(o),r.confirm("Delete Order Fail!")})},s=()=>{c.post("/api/admin/vendors",{}).then(e=>{if(e.data.code==200&&e.data.data.success==1)for(let o=0;o<e.data.data.vendors.length;o++)t.value.push({vendor_id:e.data.data.vendors[o].vendor_id,vendor_display_name:e.data.data.vendors[o].vendor_display_name,product_count:e.data.data.vendors[o].product_count});else throw new Error("Get Products Fail!")}).catch(e=>{console.log(e),r.confirm("Get Products Fail!").then(()=>{location.reload()}).catch(()=>{location.reload()})})},t=h([]);return f(()=>{i.vendor_id==0?setTimeout(()=>{s()},250):s()}),(e,o)=>{const n=d("el-table-column"),u=d("el-button"),p=d("el-table");return b(),w(p,{data:t.value,style:{width:"100%",height:"100%"}},{default:l(()=>[a(n,{fixed:"",prop:"vendor_id",label:"Vendor ID",width:"100"}),a(n,{prop:"vendor_display_name",label:"Display Name",width:"150"}),a(n,{prop:"product_count",label:"Product Count",width:"100"}),a(n,{fixed:"right",label:"Operation",width:"150"},{default:l(m=>[a(u,{link:"",type:"primary",size:"small",onClick:g(C=>_(m.$index),["prevent"])},{default:l(()=>[x(" Remove ")]),_:2},1032,["onClick"])]),_:1})]),_:1},8,["data"])}}});export{M as default};