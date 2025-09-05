<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import axios from 'axios';
defineEmits(['close'])
const id = defineProps(['details'])
</script>

<template>
<div class="bg-white rounded-xl w-1/2 h-1/2 shadow-xl overflow-y-auto">
    <button @click="$emit('close')" class="w-[1.5em] m-3 float-right">
        <img src="/close.svg" />
    </button>
    <div class="clear-both">
        <h1 class="text-center font-semibold text-xl">{{ details?.name }}</h1>
        <div class="flex-1 p-4">
        <div v-for="(value, key) in details" :key="key" class="mb-3">
            <p class="text-gray-800">
                <span class="font-medium capitalize">{{ key }}:</span>
                {{ value }}
            </p>
        </div>
    </div>
           
    </div>
</div>

</template>


<style>
</style>