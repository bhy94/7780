import { defineStore } from 'pinia'

export const useStore = defineStore('main', {
    state: () => ({ 
        count: 0,
        vendor_display_name: "", 
        vendor_id: 0,
        role: "vendor"
    }),
    actions: {
        increment() {
            this.count++
        },
        set_display_name(name) {
            this.vendor_display_name = name
        },
        set_vendor_id(id) {
            this.vendor_id = id
        },
        set_role(role) {
            this.role = role
        },
    },
})