import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("http://localhost:8080")
    yield driver
    driver.quit()

def test_add_todo_item(driver):
    # TC-BB-001: Add New Todo Item
    input_box = driver.find_element(By.CSS_SELECTOR, "input.new-todo")
    input_box.send_keys("Buy milk\n")  # \n simulates Enter key
    todos = driver.find_elements(By.CSS_SELECTOR, "ul.todo-list li")
    assert any(todo.text == "Buy milk" for todo in todos), "Todo 'Buy milk' not found in list"

def test_mark_todo_completed(driver):
    # TC-BB-002: Mark Todo Completed
    # First, add a todo to ensure one exists
    input_box = driver.find_element(By.CSS_SELECTOR, "input.new-todo")
    input_box.send_keys("Test Task\n")
    checkbox = driver.find_element(By.CSS_SELECTOR, "ul.todo-list li .toggle")
    checkbox.click()
    todo = driver.find_element(By.CSS_SELECTOR, "ul.todo-list li")
    assert "completed" in todo.get_attribute("class"), "Todo not marked as completed"