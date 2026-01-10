# 🔧 Solução: Nome "Devocional Diário" não Aparece

## ❌ Problema

O endpoint da Evolution API para atualizar o nome do perfil está retornando 404:
```
Cannot PUT /profile/updateProfileName/Devocional-1
```

Isso significa que **a Evolution API pode não suportar atualização de perfil via API** na sua versão.

## ✅ Soluções

### **Solução 1: Configurar Manualmente no WhatsApp (RECOMENDADO)**

O nome do perfil precisa ser configurado **diretamente no WhatsApp**:

1. **Abra o WhatsApp** no celular/navegador conectado à instância
2. **Vá em Configurações** → **Perfil**
3. **Altere o nome** para "Devocional Diário"
4. **Salve**

Isso fará com que o nome apareça para todos os destinatários.

---

### **Solução 2: Configurar no Evolution API Manager**

Algumas versões do Evolution API permitem configurar o nome no Manager:

1. Acesse o **Evolution API Manager**
2. Vá na instância **Devocional-1**
3. Procure por **"Profile"** ou **"Perfil"**
4. Configure o nome como **"Devocional Diário"**

---

### **Solução 3: Usar vCard (Já Implementado)**

O sistema já envia vCard automaticamente para novos contatos. Isso faz com que:

- ✅ O destinatário receba um cartão de contato
- ✅ Posso salvar seu número facilmente
- ✅ Após salvar, o nome aparecerá nas próximas mensagens

**Para ativar:**
```env
SEND_VCARD_TO_NEW_CONTACTS=true
```

---

## 🎯 Recomendação

**Use a Solução 1 (configurar no WhatsApp)** + **Solução 3 (vCard automático)**:

1. Configure o nome manualmente no WhatsApp → Nome aparece imediatamente
2. Ative vCard automático → Novos contatos podem salvar facilmente

---

## 📝 Nota Técnica

A Evolution API pode ter diferentes versões com endpoints diferentes. O sistema tenta automaticamente vários endpoints, mas se nenhum funcionar, o nome precisa ser configurado manualmente.

**Isso não impede o envio de mensagens!** As mensagens continuam funcionando normalmente, apenas o nome precisa ser configurado uma vez manualmente.

---

## ✅ Verificação

Após configurar o nome manualmente:

1. Envie uma mensagem de teste
2. Verifique se o nome "Devocional Diário" aparece
3. Se aparecer, está funcionando! ✅

