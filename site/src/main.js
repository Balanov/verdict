import './style.css';
import { VerdictModel } from './verdict.js';

const messages = {
  en: {
    nav_benchmark: 'Benchmark', hero_kicker: 'TINY SEMANTIC VERIFIER FOR AI AGENTS', hero_tag: 'EXIT CODE 0 IS NOT PROOF.',
    hero_lead: 'A 197 KB model that reads a command, its output and exit code — then classifies the evidence as success, failure, blocked or unknown.',
    try_demo: 'Run the demo', code: 'Code', weights: 'Weights', stat_size: 'INT8 WEIGHTS', stat_latency: 'MEDIAN CPU INFERENCE', stat_f1: 'HELD-OUT MACRO-F1', stat_license: 'CODE + WEIGHTS',
    demo_title: 'Run it. Right here.', demo_lead: 'The actual quantized model runs locally in this tab. Your logs are never uploaded.', loading: 'Loading model…', ready: 'MODEL READY · LOCAL', load_error: 'MODEL FAILED TO LOAD',
    command: 'Command', exit_code: 'Exit code', classify: 'Classify tool outcome', verdict: 'VERDICT', result_waiting: 'Run the model to inspect the output.',
    bench_title: 'Small model. Measurable job.', bench_lead: '192 synthetic examples across 48 CLI families entirely absent from training. No production logs. No hidden test data.',
    model: 'MODEL', accuracy: 'ACCURACY ↑', size: 'SIZE ↓', median: 'MEDIAN ↓', baseline: 'Exit-code baseline',
    bench_note: 'Training: 1,440 records / 60 families. Latency: 576 predictions on Windows 11, AMD64, Python 3.12. Synthetic held-out performance is not production reliability.',
    taxonomy_title: 'Four outcomes. One JSON.', taxonomy_lead: 'A narrow contract that an agent can act on — with the uncertainty left visible.',
    success_desc: 'Positive evidence that the operation completed.', failure_desc: 'A concrete assertion, build or application failure.', blocked_desc: 'Permissions, dependencies, network or environment prevented execution.', unknown_desc: 'Zero tests, skipped work, dry runs, truncation or insufficient evidence.',
    integrate_title: 'Drop into your harness.', integrate_lead: 'Pure Python inference. No runtime dependencies, GPU, tokenizer downloads or telemetry.', read_docs: 'Read the documentation →', copy: 'Copy', copied: 'Copied',
    limits_title: 'Useful signal. Not absolute truth.', limits_lead: 'Verdict is an advisory classifier trained on synthetic, English-biased CLI output. It does not prove task completion, code correctness or safety. Keep deterministic checks and authoritative environment-state verification as the source of truth.',
    cite_title: 'Cite this work', footer_line: 'Free to fork. Free to modify. Free to ship.', footer_code: 'code + weights', footer_data: 'synthetic data',
    result_note: 'Advisory classification — verify consequential outcomes in the environment.', confidence: 'MODEL PROBABILITIES', error: 'Could not run inference. Check the inputs and reload the model.',
  },
  ru: {
    nav_benchmark: 'Benchmark', hero_kicker: 'КОМПАКТНАЯ СЕМАНТИЧЕСКАЯ ПРОВЕРКА ДЛЯ AI-АГЕНТОВ', hero_tag: 'EXIT CODE 0 — ЕЩЁ НЕ ДОКАЗАТЕЛЬСТВО.',
    hero_lead: 'Модель размером 197 КБ читает команду, её вывод и exit code — и классифицирует evidence как success, failure, blocked или unknown.',
    try_demo: 'Запустить демо', code: 'Код', weights: 'Веса', stat_size: 'ВЕСА INT8', stat_latency: 'МЕДИАННЫЙ INFERENCE НА CPU', stat_f1: 'MACRO-F1 НА HELD-OUT', stat_license: 'КОД + ВЕСА',
    demo_title: 'Проверьте. Прямо здесь.', demo_lead: 'Настоящие квантованные веса работают локально в этой вкладке. Ваши логи никуда не отправляются.', loading: 'Загрузка модели…', ready: 'МОДЕЛЬ ГОТОВА · ЛОКАЛЬНО', load_error: 'ОШИБКА ЗАГРУЗКИ МОДЕЛИ',
    command: 'Команда', exit_code: 'Exit code', classify: 'Определить результат', verdict: 'ВЕРДИКТ', result_waiting: 'Запустите модель, чтобы проверить вывод.',
    bench_title: 'Маленькая модель. Измеримая задача.', bench_lead: '192 синтетических примера из 48 семейств CLI, которых не было в обучении. Никаких production-логов и скрытых данных.',
    model: 'МОДЕЛЬ', accuracy: 'ACCURACY ↑', size: 'РАЗМЕР ↓', median: 'МЕДИАНА ↓', baseline: 'Baseline по exit code',
    bench_note: 'Обучение: 1 440 записей / 60 семейств. Задержка: 576 предсказаний на Windows 11, AMD64, Python 3.12. Результат на синтетических held-out данных не равен надёжности в production.',
    taxonomy_title: 'Четыре исхода. Один JSON.', taxonomy_lead: 'Узкий контракт для агента — с видимой неопределённостью.',
    success_desc: 'Вывод подтверждает, что операция завершена.', failure_desc: 'Конкретная ошибка assertion, сборки или приложения.', blocked_desc: 'Права, зависимости, сеть или окружение помешали выполнению.', unknown_desc: 'Ноль тестов, пропуски, dry run, обрезанный или недостаточный вывод.',
    integrate_title: 'Встройте в свой harness.', integrate_lead: 'Inference на чистом Python. Без runtime-зависимостей, GPU, загрузки токенизатора и телеметрии.', read_docs: 'Читать документацию →', copy: 'Копировать', copied: 'Скопировано',
    limits_title: 'Полезный сигнал. Не абсолютная истина.', limits_lead: 'Verdict — рекомендательный классификатор, обученный на синтетическом преимущественно англоязычном CLI-выводе. Он не доказывает выполнение задачи, корректность кода или безопасность. Источником истины должны оставаться детерминированные проверки и авторитетное состояние среды.',
    cite_title: 'Цитировать работу', footer_line: 'Форкайте. Модифицируйте. Внедряйте. Бесплатно.', footer_code: 'код + веса', footer_data: 'синтетические данные',
    result_note: 'Рекомендательная классификация — важные результаты проверяйте в среде.', confidence: 'ВЕРОЯТНОСТИ МОДЕЛИ', error: 'Не удалось выполнить inference. Проверьте входные данные и перезагрузите модель.',
  },
  zh: {
    nav_benchmark: '基准测试', hero_kicker: '面向 AI 智能体的微型语义验证器', hero_tag: '退出码 0 并不等于成功。',
    hero_lead: '197 KB 模型读取命令、输出和退出码，将证据分类为 success、failure、blocked 或 unknown。',
    try_demo: '运行演示', code: '代码', weights: '权重', stat_size: 'INT8 权重', stat_latency: 'CPU 推理中位数', stat_f1: '留出集 MACRO-F1', stat_license: '代码 + 权重',
    demo_title: '就在这里运行。', demo_lead: '真实的量化模型在此标签页本地运行。您的日志不会上传。', loading: '正在加载模型…', ready: '模型就绪 · 本地', load_error: '模型加载失败',
    command: '命令', exit_code: '退出码', classify: '判断工具结果', verdict: '判定', result_waiting: '运行模型以检查输出。',
    bench_title: '小模型，可衡量的任务。', bench_lead: '192 个合成样本，来自训练中完全未出现的 48 个 CLI 类别。没有生产日志，没有隐藏测试数据。',
    model: '模型', accuracy: '准确率 ↑', size: '大小 ↓', median: '中位数 ↓', baseline: '退出码基线',
    bench_note: '训练：1,440 条记录 / 60 个类别。延迟：Windows 11、AMD64、Python 3.12 上的 576 次预测。合成留出集成绩不代表生产可靠性。',
    taxonomy_title: '四种结果，一个 JSON。', taxonomy_lead: '智能体可执行的精简协议，同时保留不确定性。',
    success_desc: '有积极证据表明操作已完成。', failure_desc: '明确的断言、构建或应用失败。', blocked_desc: '权限、依赖、网络或环境阻止了执行。', unknown_desc: '零测试、跳过、试运行、截断或证据不足。',
    integrate_title: '接入您的执行框架。', integrate_lead: '纯 Python 推理。无运行时依赖、GPU、分词器下载或遥测。', read_docs: '阅读文档 →', copy: '复制', copied: '已复制',
    limits_title: '有用信号，并非绝对真相。', limits_lead: 'Verdict 是基于合成、偏英语 CLI 输出训练的辅助分类器。它不能证明任务完成、代码正确或安全。确定性检查和权威环境状态仍是事实依据。',
    cite_title: '引用此工作', footer_line: '自由复刻、修改和发布。', footer_code: '代码 + 权重', footer_data: '合成数据',
    result_note: '辅助分类——重要结果请在环境中验证。', confidence: '模型概率', error: '无法运行推理。请检查输入并重新加载模型。',
  },
  es: {
    nav_benchmark: 'Benchmark', hero_kicker: 'VERIFICADOR SEMÁNTICO MINÚSCULO PARA AGENTES DE IA', hero_tag: 'EXIT CODE 0 NO ES UNA PRUEBA.',
    hero_lead: 'Un modelo de 197 KB que lee el comando, su salida y el exit code, y clasifica la evidencia como success, failure, blocked o unknown.',
    try_demo: 'Probar la demo', code: 'Código', weights: 'Pesos', stat_size: 'PESOS INT8', stat_latency: 'INFERENCIA CPU MEDIANA', stat_f1: 'MACRO-F1 HOLD-OUT', stat_license: 'CÓDIGO + PESOS',
    demo_title: 'Pruébalo aquí mismo.', demo_lead: 'El modelo cuantizado real se ejecuta localmente en esta pestaña. Tus logs nunca se suben.', loading: 'Cargando modelo…', ready: 'MODELO LISTO · LOCAL', load_error: 'ERROR AL CARGAR EL MODELO',
    command: 'Comando', exit_code: 'Exit code', classify: 'Clasificar resultado', verdict: 'VEREDICTO', result_waiting: 'Ejecuta el modelo para inspeccionar la salida.',
    bench_title: 'Modelo pequeño. Tarea medible.', bench_lead: '192 ejemplos sintéticos de 48 familias CLI ausentes del entrenamiento. Sin logs de producción ni datos ocultos.',
    model: 'MODELO', accuracy: 'ACCURACY ↑', size: 'TAMAÑO ↓', median: 'MEDIANA ↓', baseline: 'Baseline de exit code',
    bench_note: 'Entrenamiento: 1.440 registros / 60 familias. Latencia: 576 predicciones en Windows 11, AMD64, Python 3.12. El rendimiento sintético hold-out no equivale a fiabilidad en producción.',
    taxonomy_title: 'Cuatro resultados. Un JSON.', taxonomy_lead: 'Un contrato reducido para el agente, con la incertidumbre visible.',
    success_desc: 'Evidencia positiva de que la operación terminó.', failure_desc: 'Un fallo concreto de aserción, compilación o aplicación.', blocked_desc: 'Permisos, dependencias, red o entorno impidieron la ejecución.', unknown_desc: 'Cero tests, omisiones, dry run, truncamiento o evidencia insuficiente.',
    integrate_title: 'Intégralo en tu harness.', integrate_lead: 'Inferencia en Python puro. Sin dependencias runtime, GPU, descargas de tokenizer ni telemetría.', read_docs: 'Leer la documentación →', copy: 'Copiar', copied: 'Copiado',
    limits_title: 'Señal útil. No verdad absoluta.', limits_lead: 'Verdict es un clasificador consultivo entrenado con salidas CLI sintéticas y predominantemente inglesas. No prueba que una tarea terminó, que el código es correcto ni que es seguro. Mantén comprobaciones deterministas y el estado autoritativo del entorno como fuente de verdad.',
    cite_title: 'Citar este trabajo', footer_line: 'Haz forks. Modifícalo. Distribúyelo. Gratis.', footer_code: 'código + pesos', footer_data: 'datos sintéticos',
    result_note: 'Clasificación consultiva: verifica los resultados importantes en el entorno.', confidence: 'PROBABILIDADES DEL MODELO', error: 'No se pudo ejecutar la inferencia. Revisa las entradas y recarga el modelo.',
  },
};

let language = 'en';
function setLanguage(next) {
  language = messages[next] ? next : 'en';
  document.documentElement.lang = language;
  document.querySelectorAll('[data-i18n]').forEach(node => {
    const value = messages[language][node.dataset.i18n];
    if (value) node.textContent = value;
  });
  document.querySelector('#language').value = language;
  localStorage.setItem('verdict-language', language);
  const url = new URL(location.href); url.searchParams.set('lang', language); history.replaceState(null, '', url);
}

const requested = new URLSearchParams(location.search).get('lang');
const saved = localStorage.getItem('verdict-language');
const detected = (navigator.language || 'en').toLowerCase().split('-')[0];
setLanguage(requested || saved || (messages[detected] ? detected : 'en'));
document.querySelector('#language').addEventListener('change', event => setLanguage(event.target.value));

const presets = {
  success: ['mvn test', 0, '[INFO] Tests run: 8, Failures: 0, Errors: 0\n[INFO] BUILD SUCCESS', ''],
  failure: ['npm test', 1, 'FAIL src/payments.test.js\nTests: 2 failed, 4 passed, 6 total', ''],
  blocked: ['kubectl rollout status deploy/api', 1, '', 'Error from server (Forbidden): deployments.apps "api" is forbidden'],
  unknown: ['pytest tests/', 0, 'collected 0 items\nno tests ran in 0.01s', ''],
};
let model;
const form = document.querySelector('#demo-form');
const classify = document.querySelector('#classify');

function runPrediction() {
  if (!model) return;
  try {
    const result = model.predict(
      document.querySelector('#command').value,
      Number(document.querySelector('#exit-code').value),
      document.querySelector('#stdout').value,
      document.querySelector('#stderr').value,
    );
    const label = document.querySelector('#result-label');
    label.textContent = result.label;
    label.dataset.label = result.label;
    document.querySelector('#result-note').textContent = messages[language].result_note;
    document.querySelector('#probabilities').innerHTML = `<span class="prob-title">${messages[language].confidence}</span>` + Object.entries(result.probabilities).map(([name, value]) => `
      <div class="prob-row"><span>${name}</span><div class="prob-track"><i style="width:${Math.max(0.5, value * 100)}%"></i></div><b>${(value * 100).toFixed(1)}%</b></div>`).join('');
    document.querySelector('#json-result').textContent = JSON.stringify({
      label: result.label,
      confidence: Number(result.confidence.toFixed(6)),
      advisory: true,
    }, null, 2);
  } catch (error) {
    document.querySelector('#result-note').textContent = messages[language].error;
    console.error(error);
  }
}

form.addEventListener('submit', event => { event.preventDefault(); runPrediction(); });
document.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
  const [command, code, stdout, stderr] = presets[button.dataset.preset];
  document.querySelector('#command').value = command;
  document.querySelector('#exit-code').value = code;
  document.querySelector('#stdout').value = stdout;
  document.querySelector('#stderr').value = stderr;
  runPrediction();
}));

document.querySelectorAll('[data-copy-target]').forEach(button => button.addEventListener('click', async () => {
  const text = document.getElementById(button.dataset.copyTarget).textContent;
  await navigator.clipboard.writeText(text);
  const previous = button.textContent;
  button.textContent = messages[language].copied;
  setTimeout(() => { button.textContent = previous; }, 1400);
}));

try {
  model = await VerdictModel.load(new URL('./verdict-q8.bin', document.baseURI));
  document.querySelector('#model-status').textContent = messages[language].ready;
  classify.disabled = false;
  runPrediction();
} catch (error) {
  document.querySelector('#model-status').textContent = messages[language].load_error;
  document.querySelector('#result-note').textContent = error.message;
  console.error(error);
}
