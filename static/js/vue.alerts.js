
const alertApp = Vue.createApp({
  data() {
    return {
      alerts: []
    };
  },
  methods: {
    addAlert(message, type = 'success') {
      const id = Date.now();
      this.alerts.push({ id, message, type });
      setTimeout(() => {
        this.alerts = this.alerts.filter(alert => alert.id !== id);
      }, 3000);
    }
  },
  template: `
    <div>
      <transition-group name="fade" tag="div">
        <div 
          v-for="alert in alerts" 
          :key="alert.id" 
          :class="['alert-box', alert.type]"
          @click="removeAlert(alert.id)"
        >
          {{ alert.message }}
        </div>
      </transition-group>
    </div>
  `
});

const alertInstance = alertApp.mount('#v-alerts');
// alertInstance.addAlert('Ошибка при удалении', 'error');
