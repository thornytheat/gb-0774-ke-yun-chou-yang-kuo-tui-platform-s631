const save = document.querySelector('#save-run');
save?.addEventListener('click', async () => {
  const message = document.querySelector('#feedback');
  const { run, sample, tab } = save.dataset;
  save.disabled = true;
  message.textContent = '核算中…';
  try {
    const request = run ? { method:'POST' } : {
      method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({sample}),
    };
    const res = await fetch(run ? `/api/runs/${run}/rerun` : '/api/runs', request);
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || '归档失败');
    if (run) message.textContent = '复算一致，归档编号不变。';
    else location.assign(`/survey/${tab}?${new URLSearchParams({sample,run:data.id})}`);
  } catch (error) {
    message.textContent = `${error.message}，请重试。`;
  } finally { save.disabled = false; }
});
