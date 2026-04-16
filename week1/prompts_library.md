# Prompts Library — Week 1

## Prompt 1: Basic Appointment Request
**Тип**: basic
**Промпт**:
> You are a healthcare scheduling assistant.
> A patient says: "I need to see a therapist tomorrow at 10am."
> Respond with confirmation or suggest alternatives.

**Результат**: последовательный ответ с предложением альтернатив, выглядит профессионально. Придумал имя врача (не было данных).Придумал свободные слоты (не было данных).
**Заметки**: Без роли, если промпт выглядит таким образом ("I need to see a therapist tomorrow at 10am.") - ответ не выглядит как профессиональный ответ от специалиста, а скорее как список доступных действий и контакты кризисного цента в конце (предположение на суицидальный случай на всякий).


---

## Prompt 2: Availability Check
**Тип**: basic
**Промпт**:
> You are a healthcare scheduling assistant.
> A patient asks: "What slots are available with a cardiologist this week?"
> List available time slots.

**Результат**: чёткий, структурированный ответ, без лишней "воды", только имена врачей и доступные слоты в читаемом формате. А также простой вопрос в конце с предложением забронировать даты.
**Заметки**: Тест промпта без "List available time slots." выдал "patient verification" - то есть запрос на дополнительные данные. Форматирование не выглядело профессионально (появились эмодзи). Также появилась часть про неотложные случаи (на всякий, если у пациента пристп острого инфоркта). Нет списка доступных временных слотов вообще.