import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import en from './locales/en/strings.json'
import es from './locales/es/strings.json'
import ru from './locales/ru/strings.json'

i18n
  .use(initReactI18next) // passes i18n down to react-i18next
  .init({
    resources: {
      en: {
        translation: en,
      },
      es: {
        translation: es,
      },
	  ru: {
		translation: ru,
	  },
    },
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
  })

export default i18n
