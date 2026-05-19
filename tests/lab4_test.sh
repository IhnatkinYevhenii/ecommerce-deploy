#!/bin/bash
set -e

echo "--- Starting Lab 4 Grading (Helm Check) ---"

# 1. Валідація чарта
echo "Step 1: Running helm lint..."
helm lint ./charts/ecommerce-app

# 2. Перевірка шаблонізації для Prod
echo "Step 2: Checking Production replica count..."
REPLICAS=$(helm template ecommerce ./charts/ecommerce-app -f ./charts/ecommerce-app/values-prod.yaml | grep 'replicas: 3' | xargs)
if [ "$REPLICAS" != "replicas: 3" ]; then
  echo "❌ Error: values-prod.yaml should set replicas to 3."
  exit 1
fi

# 3. Надійне тестування рендерингу (Заміна dry-run для роботи без кластера)
echo "Step 3: Testing Dry-run installation via template engine..."
helm template ecommerce ./charts/ecommerce-app --debug > /dev/null

echo "✅ SUCCESS: Lab 4 is passed!"
