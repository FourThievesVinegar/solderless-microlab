import React from 'react'
import { Form, Select } from 'semantic-ui-react'
import { useTranslation } from 'react-i18next'

import locales from '../locales/locales.json'

import './LanguageSelector.scss'

export const LanguageSelector = () => {
  const { t, i18n } = useTranslation()

  const handleLocaleChange = (e: React.SyntheticEvent, { value }: any) => {
    i18n.changeLanguage(value)
  }

  return (
    <Form>
      <Select options={locales} placeholder={t('locale')} onChange={handleLocaleChange} value={i18n.resolvedLanguage} />
    </Form>
  )
}
