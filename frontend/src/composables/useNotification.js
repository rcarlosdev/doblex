import { ref } from 'vue';

export function useNotification(autoCloseDuration = 5000) {
  const notification = ref({
    type: '',
    text: '',
    visible: false
  });

  let timeoutId = null;

  const showNotification = (type, text) => {
    if (timeoutId) clearTimeout(timeoutId);
    notification.value = {
      type,
      text,
      visible: true
    };
    if (autoCloseDuration > 0) {
      timeoutId = setTimeout(() => {
        clearNotification();
      }, autoCloseDuration);
    }
  };

  const showSuccess = (text) => showNotification('success', text);
  const showError = (text) => showNotification('error', text);

  const clearNotification = () => {
    notification.value.visible = false;
    notification.value.text = '';
    notification.value.type = '';
  };

  return {
    notification,
    showSuccess,
    showError,
    clearNotification
  };
}
