import { defineStore } from 'pinia'

export const useStore = defineStore('main', {
    state: () => ({ 
        count: 0,
        user_display_name: "", 
        user_id: 0,
        role: "user",
        charts: [ ],
    }),
    getters: {
        chart_length(state) {
            return this.charts.length
        },
        chart_total_price(state) {
            let sum = 0;
            for (let i = 0; i < this.charts.length; i++) {
                sum += (this.charts[i].price * this.charts[i].quantity)
            }
            return sum
        }
    },
    actions: {
        increment() {
            this.count++
        },
        echo() {
            console.log(this.count, "echo from store")
        },
        set_user_display_name(name) {
            this.user_display_name = name
        },
        set_user_id(id) {
            this.user_id = id
        },
        set_role(role) {
            this.role = role
        },
        add_chart(item) {
            this.charts.push(item)
        },
        chart_remove_item(item) {
            for (let i = 0; i < this.charts.length; i++) {
                if (this.charts[i].product_id == item.product_id && this.charts[i].quantity == item.quantity) {
                    this.charts.splice(i, 1)
                    // console.log("item removed from chart")
                    break
                }
            }
        },
        clear_charts() {
            this.charts = []
        }
    },
})