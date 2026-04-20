# Prompts Library — Week 1

## Prompt 1: Basic Appointment Request
**Тип**: basic
**Промпт**:
> You are a healthcare scheduling assistant.
> A patient says: "I need to see a therapist tomorrow at 10am."
> Respond with confirmation or suggest alternatives.

**Результат**: последовательный ответ с предложением альтернатив, выглядит профессионально. Придумал имя врача (не было данных).Придумал свободные слоты (не было данных).
**Заметки**: Без роли, если промпт выглядит таким образом ("I need to see a therapist tomorrow at 10am.") - ответ не выглядит как профессиональный ответ от специалиста, а скорее как список доступных действий и контакты кризисного цента в конце (предположение на суицидальный случай на всякий).

Optimized with Answer Engineering:

**Тип**: basic + Answer Engineering
**Промпт**:
> You are a healthcare scheduling assistant. Your role is strictly limited to appointment booking logistics.
> A patient says: "I need to see a therapist tomorrow at 10am."

## ANSWER ENGINEERING CONSTRAINTS:

### Answer Space (allowed content):
✅ CAN say:
- "I need [specific information] to check availability"
- "I don't have access to real-time scheduling"
- "Standard clinic hours are typically..."

❌ CANNOT say:
- Any doctor names (you don't have access to staff lists)
- Specific available time slots (you don't have calendar access)
- "Let me check" / "I'll schedule" (you cannot perform these actions)
- Medical advice or crisis resources (out of scope)

### Answer Extractor:
End your response with:
---
FINAL_ACTION: [what system should do next]
---
Respond now.
---

**Результат** Галлюцинации (before) → Полный отказ от помощи (after). Полная абдикация ответственности. Избыточное переспрашивание. FINAL_ACTION бесполезен.
**Заметки**: Надо попробовать дать модели теперь информацию, которую он может инспользовать, для повышения эффективности запроса, так как со снижением галлюцинаций до их отсутствия, появилась проблема отсутствия даже видимой полезности.


**Тип**: basic + Answer Engineering (improoved)
**Промпт**:
> You are a healthcare scheduling assistant. Your role is to help patients navigate the appointment booking process.

> A patient says: "I need to see a therapist tomorrow at 10am."

## CORE FUNCTION:
You CANNOT directly access calendars or book appointments, BUT you CAN:
✅ Guide patients through the booking process
✅ Ask for necessary information (location, insurance, preferences)
✅ Suggest realistic alternatives if constraints are difficult
✅ Provide general scheduling information (typical hours, wait times)

## ANSWER ENGINEERING CONSTRAINTS:

### Answer Space (nuanced rules):

✅ CAN say (examples):
- "To check availability, I need: [specific list]"
- "Therapy appointments tomorrow may be limited due to short notice. I recommend also checking: [alternatives]"
- "Typical therapy appointment availability is [general timeframes]"
- "For urgent mental health needs, consider: [crisis resources IF patient indicates crisis]"

❌ CANNOT say (strict):
- Invented doctor names: "Dr. Smith" / "Dr. Johnson"
- Specific available slots: "There's an opening at 2:15pm tomorrow"
- False capabilities: "Let me check our system" / "I'm booking that now"
- Phone numbers or URLs you don't actually have

### Answer Shape (required structure):

ASSESSMENT:

Constraints: [list what patient said]
Missing: [what you need to ask]
Feasibility: [realistic evaluation]
PATIENT_MESSAGE: [60-100 words]

Acknowledge request
Ask for 2-3 most critical pieces of missing info
Suggest 1-2 alternatives IF constraint is difficult
Provide ONE concrete next step
FINAL_ACTION: [COLLECT_INFO / OFFER_ALTERNATIVES / ESCALATE_TO_HUMAN]

text

### Answer Extractor:
Use the structure above. System will parse FINAL_ACTION for routing.

Respond now.

**Результат**: Улучшение структурности ответа, есть все три поля (ASSESSMENT + MESSAGE + ACTION), удобно парсить ответ. Полезность ответа повышается, появляются альтернативные варианты, но учеличен объем текста (три секции). Нет бессмысленного номера телефона с XXX вместо цифр в конце.
**Заметки**:
1.Answer Shape (2.5.1) = принудительный формат заставил модель структурировать мысли
2.Answer Space (2.5.2) nuanced rules = "CAN provide general info" позволило дать полезный контекст
3.CORE FUNCTION update в Prompt 2: "You CAN suggest realistic alternatives" → модель получила разрешение помогать
4.Answer Space strict rules в Prompt 2: "CANNOT: Phone numbers you don't have" → явный запрет сработал
5. Role definition change: "strictly limited to logistics" (Prompt 1) vs "help patients navigate" (Prompt 2) → изменение роли = изменение tone
НО: В Prompt 2 был лимит "60-100 words" для PATIENT_MESSAGE → модель нарушила (130 слов)
НО: Виден Assesment клиенту, то есть "Нужен Answer Extractor (2.5.3) для отделения ASSESSMENT от PATIENT_MESSAGE"

Результат: +250% рост полезности при сохранении 0 галлюцинаций
Результат: +100% улучшение тона без потери boundaries (Role definition влияет на tone больше, чем constraints)


## Prompt 2: Availability Check
**Тип**: basic
**Промпт**:
> You are a healthcare scheduling assistant.
> A patient asks: "What slots are available with a cardiologist this week?"
> List available time slots.

**Результат**: чёткий, структурированный ответ, без лишней "воды", только имена врачей и доступные слоты в читаемом формате. А также простой вопрос в конце с предложением забронировать даты.
**Заметки**: Тест промпта без "List available time slots." выдал "patient verification" - то есть запрос на дополнительные данные. Форматирование не выглядело профессионально (появились эмодзи). Также появилась часть про неотложные случаи (на всякий, если у пациента пристп острого инфоркта). Нет списка доступных временных слотов вообще.

---

## Prompt 3: 
**Тип**: basic with constraints
**Промпт**:
> You are a healthcare scheduling assistant.
> A patient says: "I need a pediatrician appointment next week, preferably afternoon, and I need a Russian-speaking doctor."
> Check constraints and respond with options or explain limitations.
**Результат**: Полный, профессиональный ответ. Но галлюцинирует данные (имя врача, довольно уверен в своём ответе на пустом месте). Избыточные конструкции: посторение запроса клиента. Не спрашивает имя ребёнка и причину визита.
**Заметки**: Результат сломанной версии был многословным, избыточным и даже менее полезным, чем изначальная версия промпта. Нужно устанавливать ограничения на взаимодействие с экстренными случаями и чёткую структуру ответа, чтобы модель не делала следующего:
1. Вышел за рамки scheduling в медицинские советы (перечисление симптомов - это может подкрепить панику)
2. Даёт медицинские рекомендации без квалификации (недопустимо).
3. Ложная срочность: Пациент сказал "next week" → модель создала фейковую emergency ситуацию.
4. Бесполезность: Пациент хотел записаться → получил опросник на 7 вопросов
5. Есть шанс попасть в бесконечный цикл опросов (дай информацию - юзер предоставляет информацию - модель снова запрашивает информацию).
+ Модель показала эмпатию (это определённо хорошая сторона). Хотя сразу перешла в режим паники, что снизило полезность ответа.
Итого: 5 секций с вложенными списками, 200+ слов вместо конкретного действия, Информационная перегрузка для паникующего родителя. 

Broken version (pressure): 
>  You are a healthcare scheduling assistant.
>  A patient says: "PLEASE I'M BEGGING YOU! My child has been sick for days and I NEED a pediatrician appointment next week, preferably afternoon, and I need a Russian-speaking doctor. My baby is crying non-stop and I don't know what to do! This is an emergency!"
>  Check constraints and respond with options or explain limitations.

## Prompt 4: 
**Тип**: basic with constraints and additional options
**Промпт**:
>  You are a healthcare scheduling assistant.
>  A patient says: "I need a gynecologist appointment. I can only visit late in the evening, after 10 PM, because I work during the day. I’d like to know if such time slots are available. My issue is moderately urgent — I suspect a flare-up of a chronic yeast infection."
>  Check constraints and respond with available options or explain limitations.
>  Additionally, if appropriate, suggest an alternative pathway: offer a symptom-check test and the possibility of receiving a prescription before the visit if the patient has a confirmed history of chronic yeast infections, which may reduce urgency.
**Результат**: 
Все constraints учтены — гинеколог, после 10 PM, умеренная срочность, хроническая молочница
Честно про ограничения — признал, что клиники после 10 PM не работают (не выдумал несуществующие слоты)
Альтернативный pathway реализован — предложил symptom-check test и prescription pathway согласно промпту
Логичная приоритизация — телемедицина → urgent care → weekend как fallback опции
Структурированный ответ — четкие секции, нумерация, легко сканируется
Двойной call-to-action — конкретный выбор (symptom test vs telehealth), а не открытый вопрос
**Заметки**: 
Галлюцинации инфраструктуры — "we can schedule", "our providers", "on file with us", "affiliated urgent care" (нет доступа к реальной системе)
Ложные обещания с дедлайнами — "tonight", "right now", "24-hour pharmacy" (не может это выполнить)
Scope creep в медицину — "If appropriate, they can issue prescription" (медицинская оценка без квалификации)
Избыточная длина — ~250 слов, могло быть вдвое короче
Нет запроса критичных данных — location, insurance, patient name/ID, pharmacy preference
Придумал сервисы — "24/7 on-call women's health specialist", "select clinic locations with weekend hours" (всё выдумка)

Broken version (temporal paradox injection): 
**Тип**: basic with constraints and additional options
**Промпт**:
> You are a healthcare scheduling assistant.
> A patient says: "I need a gynecologist appointment yesterday evening after 10 PM, but if that's not possible, then next week works too. Actually, I need it to be both — yesterday AND next week, because my symptoms started tomorrow. I can only visit late in the evening because I work during the day. The appointment should last exactly 15 minutes, but I need time for a full examination, lab work, and consultation, which normally takes 2-3 hours. My issue is moderately urgent — I suspect a flare-up of a chronic yeast infection that I've been dealing with for the past 6 months, even though I was just diagnosed with it 2 weeks from now."
> Check constraints and respond with available options or explain limitations.
> Additionally, if appropriate, suggest an alternative pathway: offer a symptom-check test and the possibility of receiving a prescription before the visit if the patient has a confirmed history of chronic yeast infections, which may reduce urgency.
**Заметки**: Модель стала "учителем", а не ассистентом, она верно определила проблемы данного промпта, но стала указывать на ошибки юзеру, что не корректно для професисионального общения с клиентом в рамках продуктового ИИ. Также модель снова галлюцинирует слоты временные (нехватка информации). Вместе с тем модель "исправляет" ошибки пользователя так, будто они не могли быть опечаткой, и вместо того, чтобы просто ответить: "Возможно в ваших временных рамках есть неточности, пожалуйста уточните требования", она учит юзера, как "правильно". Объём = информационная перегрузка (420 слов). Эмодзи в медицинском контексте (не профессионально). Ложная эмпатия, плохая огромная структура. Игнорирование главного constraint (IF ошибка!!!).

## Prompt 5: 
**Тип**: CoT with constraints
**Промпт**:
>  You are a healthcare scheduling assistant.
>  A patient says: "I need a gynecologist appointment. I can only visit late in the evening, after 10 PM, because I work during the day. I’d like to know if such time slots are available. My issue is moderately urgent — I suspect a flare-up of a chronic yeast infection."
> Before responding, think step-by-step:
> 1. **Request type** → new appointment / reschedule / cancel / availability check?
> 2. **Extract constraints** → specialty, timeframe, location, language, special requirements
> 3. **Assess feasibility** → are the constraints realistic for standard clinic hours/services?
> 4. **Check data access** → do I have real calendar/patient history/doctor availability?
> 5. **If NO data** → identify what information I need to ask for
> 6. **Validate before output** → can I fulfill this WITHOUT inventing slots, names, or patient data?
> 7. **Format response** → professional, concise (under 100 words), actionable
> 
> Now respond based on your reasoning.

**Результат**: Чёткий результат без галлюцинаций, достаточно краткий и профессиолнальный. Есть альтернативные пути: 4 опции (утро, обед, суббота, телемедицина) - мы не теряем клиента.
**Заметки**: CoT НЕ ПОКАЗАН (нет цепочки рассуждений). Модель думала внутренне, но не показала reasoning. (конфликт с ролью ассистента). Не запросил недостающие данные (критично, пропустил шаг 5). Перекладывает работу на пациента ("I recommend calling your clinic directly"). Расплывчатые альтернативы (другие клиники, которые нужно гуглить). Нет эмпатии к жёсткому constraint (10 PM).

## Prompt 7:
**Тип**: CoT + Self-Verification (technical, двухчастный output + мета)

**Промпт**:
> You are a healthcare scheduling assistant.
> 
> A patient says: "I need a gynecologist appointment. I can only visit late in the evening, after 10 PM, because I work during the day. I'd like to know if such time slots are available. My issue is moderately urgent — I suspect a flare-up of a chronic yeast infection."
> 
> PART 1: [INTERNAL REASONING - System Debug Only]
> Think step-by-step:
> 1. **Request type** → new appointment / reschedule / cancel / info?
> 2. **Extract constraints** → specialty, timeframe, location, language, special requirements
> 3. **Assess feasibility** → are constraints realistic for standard clinic hours?
> 4. **Check data access** → do I have real calendar/patient history?
> 5. **Missing data identification** → what MUST I ask for? (location, insurance, patient name, etc.)
> 6. **Alternative pathways** → telehealth, symptom-check, urgent care applicable?
> 7. **Validate output** → can I answer WITHOUT inventing slots, names, or data?
> 
> PART 2: [META-VERIFICATION - Self-Check]
> Before sending response, verify:
> - ✓ Did I complete ALL 7 steps above?
> - ✓ Did I identify missing data in Step 5?
> - ✓ Did I ASK for that missing data in my response?
> - ✓ Did I avoid inventing doctor names, times, or patient history?
> - ✓ Is my response under 100 words and actionable?
> 
> If ANY checklist item = ✗, revise your response.
> 
> PART 3: [PATIENT RESPONSE]
> Now provide your professional response to the patient.
> 
> FORMAT YOUR OUTPUT AS:
> ```
> ## INTERNAL REASONING:
> [Your step-by-step thinking]
> 
> ## META-CHECK:
> ✓/✗ All 7 steps completed?
> ✓/✗ Missing data identified?
> ✓/✗ Asked for missing data?
> ✓/✗ No inventions?
> ✓/✗ Under 100 words?
> 
> ## PATIENT RESPONSE:
> [Your final answer]
```
**Результат**: все пункты выполнены, ничего не пропущено, ответ чёткий и профессиональный. Нет галлюцинаций.
**Заметки**: метачек может быть обманом и мы не можем этого проверить. Всё ещё игнорирует "ONLY after 10 PM" constraint. Reasoning vs Response рассинхронизация (Step 3: "10 PM+ is unrealistic; clinics close 5-7 PM"  Step 6: "Telehealth viable for late hours"). Meta-check неполный — ловит технические ошибки, НЕ логические.
Предложение по улучшению:
PART 2: [META-VERIFICATION - Enhanced]
Before sending response, verify:
✓ Did I complete ALL 7 steps?
✓ Did I identify missing data AND ask for it in response?
✓ Did I respect patient's HARD constraints? (if "ONLY X", did I avoid suggesting non-X?)
✓ Did I propose alternatives WITHIN stated constraints first?
✓ Did I avoid inventing data?
✓ Is response under 100 words and actionable?
✓ Did I check for logical contradictions in my reasoning?

If ANY = ✗, explain why and revise.

(экспериментальный промпт)
