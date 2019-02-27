package com.credits.baudit.contracts;

import java.util.Date;

public class Device {
	
	private final String name ;
	private final Date purchaseDate;
	private final String category;
	private final String manufacturer;
	
	public Device(String name, Date purchaseDate, String category, String manufacturer) {
		this.name = name;
		this.purchaseDate = purchaseDate;
		this.category = category;
		this.manufacturer = manufacturer;
	}

	public String getName() {
		return name;
	}

	public Date getPurchaseDate() {
		return purchaseDate;
	}

	public String getCategory() {
		return category;
	}
	
	
}
